from sst.actions import *


#for number in range(1,3):

go_to('http://censusmappingandmarketing.herokuapp.com/')
#assert_title_contains('Ubuntu')

textelement = get_element(name = "city")
check1element = get_element(name="race AfricanAmerican")
check2element = get_element(name="gender Male")
check3element = get_element(name="age 20")
submitelement = get_element(id = "submitButton")
write_textfield(textelement, "Littleton, CO", check=True, clear=True)
set_checkbox_value(check1element, True)
set_checkbox_value(check2element, True)
set_checkbox_value(check3element, True)
click_button(submitelement, wait=True)


mapelement = get_element(id="map_canvas")



value = assert_element(text = "Data processed!")
#print value


