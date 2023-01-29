from src.base_modules.routes import ParsedRoute


string = ParsedRoute.serialize('/route', {'currency': ['USD', 'EUR', 'CYN']})
parsed = ParsedRoute(string)
assert parsed.get_arg('currency')[0] == 'USD'
assert parsed.get_arg('currency')[1] == 'EUR'
assert parsed.get_arg('currency')[2] == 'CYN'
print(ParsedRoute.serialize('/route', {}))
a1 = "/send?"
a2 = "/send?drop-prev=True"
a3 = "/currency_graph?drop-prev=True&currency=Bla1Bla2Bla3"
a4 = "/send?text=новое тестовое сообщение&query=where pk_id = '439133935'"
a5 = "/try_to_break?text=новое?тестовое cooбщение&query=where pk_id = '439133935'"
p1 = ParsedRoute(a1)
p2 = ParsedRoute(a2)
p3 = ParsedRoute(a3)
p4 = ParsedRoute(a4)
p5 = ParsedRoute(a5)
print(str(p1))
print(str(p2))
print(str(p3))
print(str(p4))
print(str(p5))
assert p1.route == '/send'
assert p2.route == '/send'
assert p3.route == '/currency_graph'
assert p4.route == '/send'
assert p4.route == '/send'
assert p2.get_arg('drop-prev')[0] == 'True'
assert p3.get_arg('drop-prev')[0] == 'True'
assert p3.get_arg('currency')[0] == 'Bla1Bla2Bla3'
initial_value = "Oh i don't like any %s serializations. Let me try=to break it \"maybe like this 😀"
super_hard = ParsedRoute.serialize('/route', {
    "some_key": initial_value
})
print(ParsedRoute(super_hard).get_arg("some_key"))
assert ParsedRoute(super_hard).get_arg("some_key")[0] == initial_value
