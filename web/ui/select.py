def toArray(select, value = "value"):
    if value not in ["value", "html"]: print("value, only accepts the 'value' or 'html'"); return
    if value == "html": value="innerHTML"

    options = [x for x in select.find_elements_by_tag_name("option")]
    arrOptions = []
    # this part is cool, because it searches the elements contained inside of select_box
    # and then adds them to the list options if they have the tag name "options"

    for element in options:
        # arrOptions.append(element.get_attribute("value"))
        arrOptions.append(element.get_attribute(value))
        # or append to list or whatever you want here

    return arrOptions


def getValueOfInnerHtml(select, html):
    options = [x for x in select.find_elements_by_tag_name("option")]
    # this part is cool, because it searches the elements contained inside of select_box
    # and then adds them to the list options if they have the tag name "options"

    for element in options:
        # arrOptions.append(element.get_attribute("value"))
        if element.get_attribute("innerHTML") == html:
            return element.get_attribute("value")
        # or append to list or whatever you want here
