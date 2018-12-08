from ophyd import (Component as Cpt, DynamicDeviceComponent as DDC,
                   EpicsSignal, EpicsSignalRO)
from ophyd.areadetector.plugins import (
    PluginBase, Overlay, ColorConvPlugin, FilePlugin, HDF5Plugin, ImagePlugin,
    JPEGPlugin, MagickPlugin, NetCDFPlugin, NexusPlugin, OverlayPlugin,
    ProcessPlugin, ROIPlugin, StatsPlugin, TIFFPlugin, TransformPlugin)
from ophyd.areadetector import EpicsSignalWithRBV as SignalWithRBV, ad_group


def DDC_EpicsSignal(*items, **kw):
    return DDC(ad_group(EpicsSignal, items), **kw)


def DDC_EpicsSignalRO(*items, **kw):
    return DDC(ad_group(EpicsSignalRO, items), **kw)


def DDC_SignalWithRBV(*items, **kw):
    return DDC(ad_group(SignalWithRBV, items), **kw)


class PluginBase_V20(PluginBase):
    epics_ts_sec = Cpt(SignalWithRBV, 'EpicsTSSec')
    epics_ts_nsec = Cpt(SignalWithRBV, 'EpicsTSNsec')


class FilePlugin_V20(FilePlugin, PluginBase_V20):
    ...


class FilePlugin_V21(FilePlugin_V20):
    lazy_open = Cpt(SignalWithRBV, 'LazyOpen', string=True,
                    doc="0='No' 1='Yes'")


class FilePlugin_V22(FilePlugin_V21):
    create_directory = Cpt(SignalWithRBV, 'CreateDirectory')
    file_number = Cpt(SignalWithRBV, 'FileNumber')
    file_number_sync = None  # REMOVED
    file_number_write = None  # REMOVED
    temp_suffix = Cpt(SignalWithRBV, 'TempSuffix', string=True)


class GatherPlugin_V31(PluginBase_V20, version=(3, 1)):
    ...
