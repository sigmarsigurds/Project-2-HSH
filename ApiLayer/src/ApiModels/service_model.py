from dataclasses import dataclass


@dataclass
class ServiceModel:
    host: str
    port: int

    def get_url(self, path: str) -> str:
        """
        This function create url out of give host, port and endpoint. But in also need the last path of the url

        :param path: The last path in the url
        :return: Url with the last path given as attribute http://{self.host}:{self.port}/{self.endpoint}/attribute
        """

        if path[0] != "/":
            path = f"/{path}"

        return f"http://{self.host}:{self.port}{path}"

