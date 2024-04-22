from . import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'default.jpg')
    products = db.relationship('Product', backref='Category', cascade="all, delete-orphan")

    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {}\n" 
        str = str.format(self.id, self.name, self.description, self.image)
        return str      
    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    subname = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    size = db.Column(db.Text(64),nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    def __repr__(self):
        str = "ID: {}, Name: {}, Description: {}, Image: {}, Price: {}, Category_ID: {}\n" 
        str = str.format(self.id, self.name, self.description, self.image, self.price, self.category_id)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('product_id',db.Integer,db.ForeignKey('products.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'product_id') )

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    products = db.relationship("Product", secondary=orderdetails, backref="orders")
    
    def __repr__(self):
        str = "ID: {}, Date: {}, First Name: {}, Last name: {}, Email: {}, Phone: {},   Total Cost: {}\n" 
        str = str.format(self.id, self.date, self.firstname, self.lastname, self.email, self.phone, self.totalcost)
        return str

    

    

