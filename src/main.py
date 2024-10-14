from src.helpers import requires_python_version
from src.pipeline import AnalyzeTask, ExtractTask, FetchTask, TransformTask
from src.schemas import generate_links


@requires_python_version()
def main() -> None:
    links = generate_links()
    fetched_data = FetchTask(links).run()
    extracted_data = ExtractTask(fetched_data).run()
    transformed_data = TransformTask(extracted_data).run(mode="wait")
    AnalyzeTask(transformed_data).run()


if __name__ == "__main__":
    main()
