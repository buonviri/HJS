import pyperclip

filtered = []
discard = []
clip = pyperclip.paste()

clip = clip.replace('You count', '')
print(clip)
clip = clip.replace('with a total of', ',')
print(clip)
clip = clip.replace('wardrobe and about', 'wardrobe , about')
print(clip)
clip = clip.replace('handful ', '***HANDFUL*** ')
print(clip)
clip = clip.replace('pinch', '***PINCH***')
print(clip)
clip = clip.replace('items.', 'items,')
print(clip)
clip = clip.replace('\n', ',')
print(clip)

handfuls = clip.split(',')
for line in handfuls:
    if line.endswith('items'):
        discard.append(line.strip())
        print('END: ' + line)
    elif len(line) < 2:
        pass  # blank line
    else:
        filtered.append(line.strip())
        print(line)
pyperclip.copy('\n'.join(filtered) + '\n' + '\n'.join(discard))

"""
You count about three handfuls of ground garlic inside the large wardrobe, about nineteen handfuls of ground basil inside the large wardrobe, about eight handfuls of cloves inside the large wardrobe, about one handful of ground parsley inside the large wardrobe, about ten handfuls of ground thyme inside the large wardrobe, about seven handfuls of some curry powder inside the large wardrobe, about thirteen handfuls of ground oregano inside the large wardrobe, about nine handfuls of black pepper inside the large wardrobe, about eleven handfuls of ground sage inside the large wardrobe, about five handfuls of ground cinnamon inside the large wardrobe, about two handfuls of ground turmeric inside the large wardrobe, about twenty-one handfuls of ground coriander inside the large wardrobe, about five handfuls of ground cardamom inside the large wardrobe, about eight handfuls of sumac inside the large wardrobe, about fourteen handfuls of methi inside the large wardrobe, about sixteen handfuls of ground ginger inside the large wardrobe, about eight handfuls of ground fennel inside the large wardrobe, about six handfuls of caraway inside the large wardrobe, about seven handfuls of cumin inside the large wardrobe and about ten handfuls of saffron inside the large wardrobe with a total of one hundred and eighty-three items.
You count about seven handfuls of some curry powder inside the large wardrobe with a total of seven items.
You count about seven handfuls of sea salt inside the large wardrobe with a total of seven items.

about three handfuls of ground garlic inside the large wardrobe
about nineteen handfuls of ground basil inside the large wardrobe
about eight handfuls of cloves inside the large wardrobe
about one ***HANDFUL*** of ground parsley inside the large wardrobe
about ten handfuls of ground thyme inside the large wardrobe
about seven handfuls of some curry powder inside the large wardrobe
about thirteen handfuls of ground oregano inside the large wardrobe
about nine handfuls of black pepper inside the large wardrobe
about eleven handfuls of ground sage inside the large wardrobe
about five handfuls of ground cinnamon inside the large wardrobe
about two handfuls of ground turmeric inside the large wardrobe
about twenty-one handfuls of ground coriander inside the large wardrobe
about five handfuls of ground cardamom inside the large wardrobe
about eight handfuls of sumac inside the large wardrobe
about fourteen handfuls of methi inside the large wardrobe
about sixteen handfuls of ground ginger inside the large wardrobe
about eight handfuls of ground fennel inside the large wardrobe
about six handfuls of caraway inside the large wardrobe
about seven handfuls of cumin inside the large wardrobe
about ten handfuls of saffron inside the large wardrobe
about seven handfuls of some curry powder inside the large wardrobe
about seven handfuls of sea salt inside the large wardrobe
one hundred and eighty-three items
seven items
seven items

"""
