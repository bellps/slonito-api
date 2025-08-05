from app.types.prompt_request import PromptRequest


class PromptFormatter():
    def __init__(self, prompt_request: PromptRequest) -> None:
        self.prompt_request = prompt_request

    def format(self) -> str:
        return f"""
        {self.instructions()}
        Using the SQL schema:
        {self.prompt_request.sql_schema}
        Generate a SQL query for the following question:
        {self.prompt_request.prompt}
        """

    def instructions(self) -> str:
        return f"""
        # System Instructions

        ## Basic Rules
        You are a relational database specialist, with the focus of creating SQL queries based on a given database schema and a question from the user.

        Your output must fit following markdown format:
        ```sql
            query
        ```
        , where "query" must be replaced by the query that you created.

        The queries must follow the PostgreSQL dialect.
        If the question does not match the database schema by any chance, you must output an empty string, without the markdown format.

        <end_of_turn><start_of_turn>user
        """
