from tax_module.models import TaxableItemType, PanHolderType

INDIAN_GST_RATE_CARD = {TaxableItemType.SERVICE: 12}


INDIAN_TDS_RATE_CARD = {
    PanHolderType.P: 1,
    PanHolderType.H: 1,
    PanHolderType.A: 2,
    PanHolderType.F: 2,
    PanHolderType.T: 2,
    PanHolderType.C: 2,
}
