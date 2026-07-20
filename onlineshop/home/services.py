from home.handlers.registry import get_section_handler
from home.selectors import get_active_home_sections


def get_home_sections():
    """
    دریافت اطلاعات صفحه اصلی.
    """

    sections = []

    for section in get_active_home_sections():

        handler = get_section_handler(
            section_type=section.section_type,
        )

        sections.append(
            {
                "section": section,
                "items": handler.get_items(
                    section=section,
                ),
            }
        )

    return sections