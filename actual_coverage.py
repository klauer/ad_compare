import common_plugins
import ophyd
import ophyd.sim

for cls, pvfn in [
        # (common_plugins.CommonPlugins_V20, 'R2-0'),
        # (common_plugins.CommonPlugins_V21, 'R2-1'),
        # (common_plugins.CommonPlugins_V22, 'R2-2'),
        # (common_plugins.CommonPlugins_V23, 'R2-3'),
        # (common_plugins.CommonPlugins_V24, 'R2-4'),
        # (common_plugins.CommonPlugins_V25, 'R2-5'),
        # (common_plugins.CommonPlugins_V26, 'R2-6'),
        # (common_plugins.CommonPlugins_V31, 'R3-1'),
        # (common_plugins.CommonPlugins_V32, 'R3-2'),
        (common_plugins.CommonPlugins_V33, 'R3-3'),
        # (common_plugins.CommonPlugins_V34, 'R3-4'),
        ]:

    print('')
    print('')
    print('----------------------------------------------------------------')
    print(cls.__name__)
    plugin = ophyd.sim.make_fake_device(cls)(prefix='PREFIX:', name='test')
    plugin.wait_for_connection()

    pvs = list(walk.item.pvname for walk in plugin.walk_signals(include_lazy=True)
               if hasattr(walk.item, 'pvname'))
    pvs += list(walk.item.setpoint_pvname for walk in plugin.walk_signals(include_lazy=True)
                if hasattr(walk.item, 'setpoint_pvname'))
    pvs = set(pvs)
    print('total pvs', len(pvs))


    from_ioc = [pv.strip() for pv in open(f'pvlists/{pvfn}.txt', 'rt').readlines()]
    print('from ioc', len(from_ioc))

    missing = set(from_ioc) - pvs

    print('missing:')
    for pv in sorted(missing):
        print('\t', pv)

    print()
    print()
    print()
    print('should not exist:')
    for pv in sorted(set(pvs) - set(from_ioc)):
        print('\t', pv)
