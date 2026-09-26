import json
import xml.etree.ElementTree as ET  # noqa: N817
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class OutputStrategy(ABC):
    @abstractmethod
    def render(self, text: str) -> str:
        pass


class ConsoleOutput(OutputStrategy):
    def render(self, text: str) -> str:
        return text


class ReverseOutput(OutputStrategy):
    def render(self, text: str) -> str:
        return text[::-1]


class Serializer(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        title = ET.SubElement(root, "title")
        title.text = book.title
        content = ET.SubElement(root, "content")
        content.text = book.content
        return ET.tostring(root, encoding="unicode")


class BookPrinter:
    @staticmethod
    def display(book: Book, strategy: OutputStrategy) -> None:
        print(strategy.render(book.content))

    @staticmethod
    def print_book(book: Book, strategy: OutputStrategy) -> None:
        print(f"Printing the book: {book.title}...")
        print(strategy.render(book.content))


def main(book: Book, commands: list[tuple[str, str]]) -> str | None:
    strategies = {
        "console": ConsoleOutput(),
        "reverse": ReverseOutput(),
    }
    serializers = {
        "json": JsonSerializer(),
        "xml": XmlSerializer(),
    }

    result = None
    for cmd, method_type in commands:
        if cmd == "display":
            print(strategies[method_type].render(book.content))
        elif cmd == "print":
            print(f"Printing the book: {book.title}...")
            print(strategies[method_type].render(book.content))
        elif cmd == "serialize":
            result = serializers[method_type].serialize(book)
        else:
            raise ValueError(f"Unknown command: {cmd}")
    return result


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
