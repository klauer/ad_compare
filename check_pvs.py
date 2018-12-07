import common_plugins
import ophyd
import ophyd.sim

cls = ophyd.sim.make_fake_device(common_plugins.CommonPlugins_V21)
plugin = cls(prefix='PREFIX:', name='test')
plugin.wait_for_connection()

pvs = list(walk.item.pvname for walk in plugin.walk_signals(include_lazy=True)
           if hasattr(walk.item, 'pvname'))
pvs += list(walk.item.setpoint_pvname for walk in plugin.walk_signals(include_lazy=True)
            if hasattr(walk.item, 'setpoint_pvname'))
pvs = set(pvs)
print('total pvs', len(pvs))


from_ioc = [pv.strip() for pv in open('pvlists/R2-1.txt', 'rt').readlines()]
print('from ioc', len(from_ioc))

missing = set(from_ioc) - pvs
