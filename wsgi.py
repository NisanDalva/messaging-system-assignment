from project import getApp, getDb
app = getApp()
db = getDb()
db.create_all()