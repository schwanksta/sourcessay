import re

# List lifted from March Schaver's
# Anonymous Source Tracker: http://inkstainedwretch.com/anonymous

signs_of_weakness = [
    "sources say",
    "asked not to be quoted by name",
    "did not wish to be identified",
    "did not want to be identified",
    "declined to be identified",
    "refused to be identified",
    "an anonymous source",
    "asked not to be identified",
    "declined to give her name",
    "declined to give his name",
    "condition of anonymity",
    "requested anonymity",
    "asked that his name not be used",
    "asked that her name not be used",
    "refused to give her name",
    "refused to give his name",
    "sources close to",
    "source close to",
    "asked not to be named",
    "declined to be named",
    "refused to be named",
    "wouldn't give his name",
    "wouldn't give her name",
    "spoke on background",
    "speaking on background",
    "spoke off the record",
    "speaking off the record",
    "speak off the record",
    "comment off the record",
    "would not speak for attribution",
    "declined to speak for attribution",
    "refused to speak for attribution",
    "asked to remain anonymous",
    "the source said",
    "a source said",
    "sources said",
    "according to people familiar with",
    "an official close to",
    "a person briefed on the matter",
    "insisted on anonymity",
    "chose to remain anonymous"
]
