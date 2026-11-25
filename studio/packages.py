"""Packages shown on the Packages page.

To change a price or a list item, edit it here and reload the site.
Prices are fixed per package (never per hour), in euro.
"""

REVISIONS = "2 rounds of changes"
REVISION_DAYS = 2  # working days for each round of changes

PACKAGE_GROUPS = [
    {
        "title": "Ads",
        "intro": "Ready-to-use ads: headline, text and a button to act.",
        "packages": [
            {
                "name": "1 Ad",
                "days": 3,
                "price": 30,
                "features": [
                    "1 ad written for your business",
                    "3 headline options",
                    "Starts from your customer's problem",
                    REVISIONS,
                ],
                "highlight": False,
            },
            {
                "name": "3 Ads",
                "days": 3,
                "price": 75,
                "features": [
                    "3 ads, each for a different offer or customer",
                    "Headlines and buttons for each",
                    REVISIONS,
                ],
                "highlight": False,
            },
        ],
    },
    {
        "title": "Social media posts",
        "intro": "Posts with text and a clear next step for your followers.",
        "packages": [
            {
                "name": "Starter Posts",
                "days": 3,
                "price": 45,
                "features": [
                    "4 posts for Instagram and Facebook",
                    "Text and call to action for each",
                    REVISIONS,
                ],
                "highlight": False,
            },
            {
                "name": "Growth Pack",
                "days": 5,
                "price": 110,
                "features": [
                    "8 posts",
                    "1 carousel (post with several images)",
                    "2 Reels scripts",
                    REVISIONS,
                ],
                "highlight": True,
            },
            {
                "name": "Full Month",
                "days": 7,
                "price": 200,
                "features": [
                    "12 posts",
                    "2 carousels",
                    "4 Reels scripts",
                    REVISIONS,
                ],
                "highlight": False,
            },
        ],
    },
]
