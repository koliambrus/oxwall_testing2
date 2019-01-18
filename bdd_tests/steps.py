from pytest_bdd import given, when, then

from value_models.status import Status


@given("initial amount of status in Oxwall database")
def old_status_amount(db):
    return db.count_news()


@given("I as a logged user")
def signed_in_user(app, admin):
    app.login_as(admin)
    yield admin
    app.logout_as(admin)


@given("I want to add status with <text>")
def status(text):
    return Status(text=text, user=signed_in_user)


@when("I add this status in Dashboard page")
def add_status(app, status):
    app.dash_page.status_text_field.input(status.text)
    app.dash_page.send_button.click()
    app.dash_page.wait_until_new_status_appeared()


@then("a new status block appears before old list of status")
def wait_new_news(app, db, old_status_amount):
    assert app.dash_page.wait_until_new_status_appeared()
    assert db.count_news() == old_status_amount + 1


@then('this status block has this <text> and author as this user and time "within 1 minute"')
def verify_status_block(app, status, signed_in_user):
    new_status = app.dash_page.status_list[0]
    assert status.text == new_status.text
    assert signed_in_user.real_name == new_status.user
    assert "within 1 minute" == new_status.time