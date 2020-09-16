from starlette.staticfiles import StaticFiles

class SpaStaticFiles(StaticFiles):
    """
    Staticfiles for single-page-apps

    Wraps the base `lookup_path` to fallback to the root `index.html` so
    the JavaScript router takes over.
    https://github.com/encode/starlette/blob/d6d0f83d3fae766cee79aa444986e83c267a3a05/starlette/staticfiles.py#L145
    """

    async def lookup_path(self, path):
        full_path, stat_result = await super().lookup_path(path)
        if stat_result is None:
            return await super().lookup_path("./index.html")

        return full_path, stat_result
