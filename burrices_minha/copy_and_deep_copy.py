import copy

house = {
    "width": 12,
    "length": 8,
    "height": 3.5,
    "doors": [
        {"type": " ENTRANCE", "width": 0.9, "height": 2.2},
        {"type": "BACK DOOR", "width": 0.7, "height": 2.0},
    ],
}

same_house = copy.deepcopy(house)
print(house)
print(same_house)
print(house == same_house)

"""
{'width': 12, 'length': 8, 'height': 3.5, 'doors': [{'type': ' ENTRANCE', 'width': 0.9, 'height': 2.2}, {'type': 'BACK DOOR', 'width': 0.7, 'height': 2.0}]}
{'width': 12, 'length': 8, 'height': 3.5, 'doors': [{'type': ' ENTRANCE', 'width': 0.9, 'height': 2.2}, {'type': 'BACK DOOR', 'width': 0.7, 'height': 2.0}]}
True
"""

house["height"] = 4.0
print(house)
print(same_house)
print(house == same_house)

"""
{'width': 12, 'length': 8, 'height': 4.0, 'doors': [{'type': ' ENTRANCE', 'width': 0.9, 'height': 2.2}, {'type': 'BACK DOOR', 'width': 0.7, 'height': 2.0}]}
{'width': 12, 'length': 8, 'height': 3.5, 'doors': [{'type': ' ENTRANCE', 'width': 0.9, 'height': 2.2}, {'type': 'BACK DOOR', 'width': 0.7, 'height': 2.0}]}
False
"""
