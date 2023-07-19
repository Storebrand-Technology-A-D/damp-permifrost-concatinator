def test_generate_ar_from_db(databases_object, accsess_roles_object):
    databases_object.spesification.pop("database3") # removed to match accsess_roles_object.spesification
    accsess_roles = databases_object.generate_accsess_roles()
    assert accsess_roles == accsess_roles_object.spesification