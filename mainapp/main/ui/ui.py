from palletizing.Pallet import Pallet
from palletizing.Item import Item


def init_pallet(
    item_WHD=[50, 80, 50], pallet_WH=[200, 200], layer=3, space=10, loader=100
):

    pallet_WHD = [pallet_WH[0], pallet_WH[1], layer * item_WHD[-1]]

    itemno = "0"
    # space = 1
    pallet = Pallet(pallet_WHD, loader, space)
    item = Item(itemno, item_WHD, weight=1, space=2)
    for i in range(18):
        item.itemno = f"{i}"
        pallet.addItem(item)
    position = pallet.putItem(item)
    return position
