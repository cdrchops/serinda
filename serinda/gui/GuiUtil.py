
class GuiUtil:
    def __init__(self):
        '''
            This class is for CRUD operations involving placing the widgets on the frontend
            So all voice commands to move a div to a different location on the page and then saving the layout
            There will be a default value for each object - like where it would be on a brand new startup
            widgetName = the html element id
            The user can say "move <widgetName> up 10 and left 40" or "move <widgetName> x 50 and y 200"
            I don't know if I can create new widgets that can be written to the page or not
            I'm sure if I try I can figure out how to do so - like <make new widget named california> which is then appended
                to the main div - then the javascript would have to be added to the javascript file to fetch whatever is needed
                and then the flask accessor would have to be added to the python file.
                I can probably figure out how to do this automagically

            Figure out the intents that would be needed and how they'd be structured
        '''
