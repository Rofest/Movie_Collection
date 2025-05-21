from typing import Dict, List, Iterator, Optional


class Film:
    def __init__(self, title: str, director: str, year: int, genre: str) -> None:
        self.title: str = title
        self.director: str = director
        self.year: int = year
        self.genre: str = genre

    def __str__(self) -> str:
        return f"{self.title} ({self.year}), режиссер: {self.director}, жанр: {self.genre}"

    def __repr__(self) -> str:
        return f"Film(title={self.title!r}, director={self.director!r}, year={self.year}, genre={self.genre!r})"


class FilmCollection(Iterator[Film]):
    def __init__(self) -> None:
        self._films: Dict[str, Film] = {}
        self._iter_titles: List[str] = []
        self._iter_index: int = 0

    def add_film(self, film: Film) -> None:
        self._films[film.title] = film

    def remove_film(self, title: str) -> bool:
        if title in self._films:
            del self._films[title]
            return True
        return False

    def search_by_title(self, title: str) -> Optional[Film]:
        return self._films.get(title)

    def search(self,
               title: Optional[str] = None,
               director: Optional[str] = None,
               year: Optional[int] = None,
               genre: Optional[str] = None) -> List[Film]:
        results: List[Film] = []
        for film in self._films.values():
            if title and title.lower() not in film.title.lower():
                continue
            if director and director.lower() not in film.director.lower():
                continue
            if year and film.year != year:
                continue
            if genre and genre.lower() not in film.genre.lower():
                continue
            results.append(film)
        return results

    def list_films(self) -> List[Film]:
        return list(self._films.values())

    def __iter__(self) -> Iterator[Film]:
        self._iter_titles = list(self._films.keys())
        self._iter_index = 0
        return self

    def __next__(self) -> Film:
        if self._iter_index < len(self._iter_titles):
            title = self._iter_titles[self._iter_index]
            self._iter_index += 1
            return self._films[title]
        raise StopIteration


def print_menu() -> None:
    print("\n=== Меню управления коллекцией фильмов ===")
    print("1. Добавить фильм")
    print("2. Удалить фильм")
    print("3. Поиск фильмов")
    print("4. Показать все фильмы")
    print("5. Перебрать коллекцию")
    print("6. Выход")


def main() -> None:
    collection = FilmCollection()

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Название: ")
            director = input("Режиссер: ")
            year_str = input("Год: ")
            genre = input("Жанр: ")
            try:
                year = int(year_str)
            except ValueError:
                print("Ошибка: год должен быть числом.")
                continue
            film = Film(title, director, year, genre)
            collection.add_film(film)
            print(f"Фильм '{title}' добавлен.")

        elif choice == '2':
            title = input("Название фильма для удаления: ")
            if collection.remove_film(title):
                print(f"Фильм '{title}' удален.")
            else:
                print(f"Фильм '{title}' не найден.")

        elif choice == '3':
            print("Введите критерии поиска (оставьте пустым для пропуска):")
            title = input("Название: ") or None
            director = input("Режиссер: ") or None
            year_input = input("Год: ") or None
            genre = input("Жанр: ") or None
            year = None
            if year_input:
                try:
                    year = int(year_input)
                except ValueError:
                    print("Ошибка: год должен быть числом.")
                    continue
            results = collection.search(title=title, director=director, year=year, genre=genre)
            if results:
                print(f"Найдено {len(results)} фильмов:")
                for film in results:
                    print(f" - {film}")
            else:
                print("Фильмы по заданным критериям не найдены.")

        elif choice == '4':
            films = collection.list_films()
            if films:
                print("Все фильмы в коллекции:")
                for film in films:
                    print(f" - {film}")
            else:
                print("Коллекция фильмов пуста.")

        elif choice == '5':
            print("Перебор коллекции фильмов:")
            for film in collection:
                print(f" -> {film}")

        elif choice == '6':
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
