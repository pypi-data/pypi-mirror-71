# bootstrap-table-py
Python wrapper for bootstrap-table.

## Usage
Declaring the table
```
class TestTable(BootstrapTable):
    name = Column('Name', width=2)
    profile = LinkColumn('profile', width=5)
    registered = DateColumn('Registered')
    delete_link = BtnColumn('Delete', hide_if=no_del_perm)

    @property
    def toolbar(self):
        if no_create_perm():
            return
        href = url_for(".user_create")
        return button_toolbar("User", href)
```

Instantiating:
```
return render_template('user.html',
           table=TestTable(data_url=url_for("users_json")),
       )
```

Rendering:
```
{{ table.render("test_table_id") }}
```

Data endpoint:
```
return jsonify(items=[{
    'name': user.name,
    'registered': datetime_format(user.registered, formatter=datetime_filter),
    'profile': {
        'href': url_for('user_show', user_id=user.id),
        'title': user.name
    },
    'delete_link': {
        'href': url_for('user_delete', user_id=user.id),
        'title': "Delete",
        'icon': 'glyphicon-trash',
        'btn-class': 'btn-danger'
    }} for user in get_users()])

```
