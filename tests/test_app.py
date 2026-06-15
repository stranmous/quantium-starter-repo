from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")
    assert "Soul Foods Pink Morsel Sales Visualiser" in header.text


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)

    chart = dash_duo.wait_for_element("#sales-chart")
    assert chart is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-filter")
    radio_buttons = dash_duo.find_elements("#region-filter input[type='radio']")
    assert len(radio_buttons) == 5