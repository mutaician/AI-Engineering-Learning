# pylint: skip-file
# flake8: noqa
# type: ignore
AgentHistoryList(
    all_results=[
        ActionResult(
            is_done=False,
            success=None,
            error=None,
            attachments=None,
            long_term_memory="Searched Google for 'gaming laptops jumia kenya'",
            extracted_content='🔍  Searched for "gaming laptops jumia kenya" in Google',
            include_extracted_content_only_once=False,
            include_in_memory=True
        ),
        ActionResult(
            is_done=False,
            success=None,
            error=None,
            attachments=None,
            long_term_memory='Clicked button with index 32: Gaming Laptops Available at Best Price Online',
            extracted_content='Clicked button with index 32: Gaming Laptops Available at Best Price Online',
            include_extracted_content_only_once=False,
            include_in_memory=True
        ),
        ActionResult(
            is_done=False,
            success=None,
            error=None,
            attachments=None,
            long_term_memory='Clicked button with index 37: Sort by:\nPopularity',
            extracted_content='Clicked button with index 37: Sort by:\nPopularity',
            include_extracted_content_only_once=False,
            include_in_memory=True
        ),
        ActionResult(
            is_done=False,
            success=None,
            error=None,
            attachments=None,
            long_term_memory='Clicked button with index 41: Price: High to Low',
            extracted_content='Clicked button with index 41: Price: High to Low',
            include_extracted_content_only_once=False,
            include_in_memory=True
        ),
        ActionResult(
            is_done=True,
            success=True,
            error=None,
            attachments=[],
            long_term_memory='Task completed: True - The price of the first gaming laptop on Jumia Kenya, sorted by the highest price, is KSh 390,000.',
            extracted_content='The price of the first gaming laptop on Jumia Kenya, sorted by the highest price, is KSh 390,000.',
            include_extracted_content_only_once=False,
            include_in_memory=False
        )
    ],
    all_model_outputs=[
        {
            'search_google': {'query': 'gaming laptops jumia kenya'},
            'interacted_element': None
        },
        {
            'click_element_by_index': {'index': 32},
            'interacted_element': DOMHistoryElement(
                tag_name='a',
                xpath='html/body/div[3]/div/div[12]/div/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div/span/a',
                highlight_index=32,
                entire_parent_branch_path=[
                    'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'div', 'span', 'a'
                ],
                attributes={
                    'jsname': 'UWckNb',
                    'href': 'https://www.jumia.co.ke/mlp-k-gaming-laptop/?srsltid=AfmBOor5Kgt1M683YZNDRH6nEKuj3yu0YDid6W7kPkSug-zvIW6TmBQK',
                    'data-ved': '2ahUKEwjC2MGf_qCOAxUskYkEHQZnAAUQFnoECBUQAQ',
                    'ping': '/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.jumia.co.ke/mlp-k-gaming-laptop/%3Fsrsltid%3DAfmBOor5Kgt1M683YZNDRH6nEKuj3yu0YDid6W7kPkSug-zvIW6TmBQK&ved=2ahUKEwjC2MGf_qCOAxUskYkEHQZnAAUQFnoECBUQAQ'
                },
                shadow_root=False,
                css_selector='html > body > div:nth-of-type(3) > div > div:nth-of-type(12) > div > div > div:nth-of-type(2) > div:nth-of-type(2) > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div > div > span > a[href="https://www.jumia.co.ke/mlp-k-gaming-laptop/?srsltid=AfmBOor5Kgt1M683YZNDRH6nEKuj3yu0YDid6W7kPkSug-zvIW6TmBQK"]',
                page_coordinates=None,
                viewport_coordinates=None,
                viewport_info=None
            )
        },
        {
            'click_element_by_index': {'index': 37},
            'interacted_element': DOMHistoryElement(
                tag_name='label',
                xpath='html/body/div[1]/main/div[2]/div[3]/section/header/div/div/label',
                highlight_index=37,
                entire_parent_branch_path=[
                    'div', 'main', 'div', 'div', 'section', 'header', 'div', 'div', 'label'
                ],
                attributes={
                    'class': 'trig -df -i-ctr',
                    'for': 'dpdw-sort'
                },
                shadow_root=False,
                css_selector='html > body > div:nth-of-type(1) > main > div:nth-of-type(2) > div:nth-of-type(3) > section > header > div > div > label.trig[for="dpdw-sort"]',
                page_coordinates=None,
                viewport_coordinates=None,
                viewport_info=None
            )
        },
        {
            'click_element_by_index': {'index': 41},
            'interacted_element': DOMHistoryElement(
                tag_name='a',
                xpath='html/body/div[1]/main/div[2]/div[3]/section/header/div/div/div/div/article/div[4]/a',
                highlight_index=41,
                entire_parent_branch_path=[
                    'div', 'main', 'div', 'div', 'section', 'header', 'div', 'div', 'div', 'div', 'article', 'div', 'a'
                ],
                attributes={
                    'class': 'fk-rad -me-start',
                    'href': '/mlp-k-gaming-laptop/?sort=highest-price#catalog-listing'
                },
                shadow_root=False,
                css_selector='html > body > div:nth-of-type(1) > main > div:nth-of-type(2) > div:nth-of-type(3) > section > header > div > div > div > div > article > div:nth-of-type(4) > a.fk-rad[href="/mlp-k-gaming-laptop/?sort=highest-price#catalog-listing"]',
                page_coordinates=None,
                viewport_coordinates=None,
                viewport_info=None
            )
        },
        {
            'done': {
                'text': 'The price of the first gaming laptop on Jumia Kenya, sorted by the highest price, is KSh 390,000.',
                'success': True
            },
            'interacted_element': None
        }
    ]
)