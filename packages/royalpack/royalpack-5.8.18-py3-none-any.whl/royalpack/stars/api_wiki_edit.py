import uuid
import royalnet.utils as ru
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import WikiPage


class ApiWikiEditStar(ApiStar):
    path = "/api/wiki/edit/v1"

    methods = ["POST"]

    summary = "Edit the contents of a wiki page, or create a new one."

    parameters = {
        "id": "The id of the wiki page to edit. Leave empty to create a new one.",
        "title": "The new title of the wiki page.",
        "contents": "The new contents of the wiki page.",
        "format": "The format of the wiki page. The default is markdown.",
        "theme": "The theme of the wiki page. The default is default."
    }

    requires_auth = True

    tags = ["wiki"]

    async def api(self, data: ApiData) -> ru.JSON:
        page_id = data.get("id")
        title = data["title"]
        contents = data["contents"]
        format = data["format"]
        theme = data["theme"]

        WikiPageT = self.alchemy.get(WikiPage)

        user = await data.user()
        if not (user.role == "Admin" or user.role == "Member" or user.role == "Bot"):
            raise ForbiddenError("You do not have sufficient permissions to edit this page.")

        if page_id is None:
            page = WikiPageT(
                page_id=uuid.uuid4(),
                title=title,
                contents=contents,
                format=format,
                theme=theme
            )
            data.session.add(page)
        else:
            page = await ru.asyncify(
                data.session
                    .query(WikiPageT)
                    .filter_by(page_id=uuid.UUID(page_id))
                    .one_or_none
            )
            if page is None:
                raise NotFoundError(f"No page with the id {repr(page_id)} found.")
            page.title = title
            page.contents = contents
            page.format = format
            page.theme = theme

        await data.session_commit()
        return page.json_full()
