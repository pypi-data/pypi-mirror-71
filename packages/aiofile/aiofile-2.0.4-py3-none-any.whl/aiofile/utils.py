import asyncio
import io
import typing
from collections.abc import AsyncIterable

from .aio import AIOFile


class Reader(AsyncIterable):
    __slots__ = "_chunk_size", "__offset", "file", "__lock"

    def __init__(
        self, aio_file: AIOFile,
        offset: int = 0, chunk_size: int = 32 * 1024,
    ):

        self._chunk_size = int(chunk_size)
        self.__offset = int(offset)
        self.file = aio_file
        self.__lock = asyncio.Lock()

    async def read_chunk(self):
        async with self.__lock:
            for retry in range(4):
                try:
                    chunk = await self.file.read(
                        self._chunk_size + retry,
                        self.__offset
                    )
                except UnicodeDecodeError:
                    if retry == 3:
                        raise
                else:
                    break

            if isinstance(chunk, str):
                chunk_size = len(chunk.encode())
            else:
                chunk_size = len(chunk)

            self.__offset += chunk_size

            return chunk

    async def __anext__(self):
        chunk = await self.read_chunk()

        if not chunk:
            raise StopAsyncIteration(chunk)

        return chunk

    def __aiter__(self):
        return self


class Writer:
    __slots__ = "__chunk_size", "__offset", "__aio_file", "__lock"

    def __init__(self, aio_file: AIOFile, offset: int = 0):
        self.__offset = int(offset)
        self.__aio_file = aio_file
        self.__lock = asyncio.Lock()

    async def __call__(self, data):
        async with self.__lock:
            await self.__aio_file.write(data, self.__offset)
            if isinstance(data, str):
                self.__offset += len(data.encode())
            else:
                self.__offset += len(data)


class LineReader(AsyncIterable):
    def __init__(
        self, aio_file: AIOFile, offset: int = 0,
        chunk_size: int = 255, line_sep: str = "\n",
    ):

        self.__reader = Reader(aio_file, chunk_size=chunk_size, offset=offset)
        self._buffer = (
            io.BytesIO() if aio_file.mode.binary else io.StringIO()
        )   # type: typing.Any
        self.linesep = (
            line_sep.encode() if self.__reader.file.mode.binary else line_sep
        )

    async def readline(self) -> typing.Union[str, bytes]:
        while True:
            chunk = await self.__reader.read_chunk()

            if chunk:
                if self.linesep not in chunk:
                    self._buffer.write(chunk)
                    continue

                self._buffer.write(chunk)

            self._buffer.seek(0)
            line = self._buffer.readline()
            tail = self._buffer.read()

            self._buffer.seek(0)
            self._buffer.truncate(0)
            self._buffer.write(tail)

            return line

    async def __anext__(self) -> typing.Union[bytes, str]:
        line = await self.readline()

        if not line:
            raise StopAsyncIteration(line)

        return line

    def __aiter__(self) -> "LineReader":
        return self
