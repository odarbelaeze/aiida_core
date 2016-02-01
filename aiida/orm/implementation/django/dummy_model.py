

from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import (
    Column,
    Integer, String, DateTime, Float, Boolean,
    ForeignKey, UniqueConstraint, 
    create_engine, Boolean, text, Text,
    or_, not_, and_, except_, except_all,
    select, func
)

from sqlalchemy.orm import (
    relationship, backref, column_property,
    sessionmaker, with_polymorphic, aliased,
    scoped_session, join, outerjoin, mapper, foreign
)

from sqlalchemy.dialects.postgresql import UUID, JSONB

from aiida.orm.implementation.django.node import Node
from aiida.common.setup import get_profile_config
from aiida.backends import settings
from aiida.backends.sqlalchemy.models.utils import uuid_func
from aiida.utils import timezone
from aiida.common.exceptions import DbContentError, MissingPluginError

from aiida.orm.implementation.calculation import from_type_to_pluginclassname
from aiida.common.pluginloader import load_plugin

Base = declarative_base()

from aiida.backends.djsite.db.models import DbNode as DjangoNode

class DbLink(Base):
    __tablename__ = "db_dblink"

    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey('db_dbnode.id', deferrable=True, initially="DEFERRED"))
    output_id = Column(Integer, ForeignKey('db_dbnode.id', ondelete="CASCADE", deferrable=True, initially="DEFERRED"))

    input = relationship("DbNode", primaryjoin="DbLink.input_id == DbNode.id")
    output = relationship("DbNode", primaryjoin="DbLink.output_id == DbNode.id")

    label = Column(String(255), index=True, nullable=False)


class DbPath(Base):
    __tablename__ = "db_dbpath"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('db_dbnode.id', deferrable=True, initially="DEFERRED"))
    child_id = Column(Integer, ForeignKey('db_dbnode.id', deferrable=True, initially="DEFERRED"))

    parent = relationship("DbNode", primaryjoin="DbPath.parent_id == DbNode.id",
                          backref="child_paths")
    child = relationship("DbNode", primaryjoin="DbPath.child_id == DbNode.id",
                         backref="parent_paths")

    depth = Column(Integer)

    entry_edge_id = Column(Integer)
    direct_edge_id = Column(Integer)
    exit_edge_id = Column(Integer)


class DbNode(Base):
    __tablename__ = "db_dbnode"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid_func)

    type = Column(String(255), index=True)
    label = Column(String(255), index=True, nullable=True)
    description = Column(Text(), nullable=True)

    ctime = Column(DateTime(timezone=True), default=timezone.now)
    mtime = Column(DateTime(timezone=True), default=timezone.now)

    dbcomputer_id = Column(Integer, ForeignKey('db_dbcomputer.id', deferrable=True, initially="DEFERRED"),
                         nullable=True)
    dbcomputer = relationship('DbComputer', backref=backref('dbnodes', passive_deletes=True))

    user_id = Column(Integer, ForeignKey('db_dbuser.id', deferrable=True, initially="DEFERRED"), nullable=False)
    user = relationship('DbUser', backref='dbnodes')

    public = Column(Boolean, default=False)

    nodeversion = Column(Integer, default=1)
    
    attributes = relationship(
        'DbAttribute',
        uselist = True,
    )


    outputs = relationship("DbNode", secondary="db_dblink",
                           primaryjoin="DbNode.id == DbLink.input_id",
                           secondaryjoin="DbNode.id == DbLink.output_id",
                           backref=backref("inputs", passive_deletes=True),
                           passive_deletes=True)

    children = relationship("DbNode", secondary="db_dbpath",
                               primaryjoin="DbNode.id == DbPath.parent_id",
                               secondaryjoin="DbNode.id == DbPath.child_id",
                               backref="parents")
    def get_aiida_class(self):
        """
        Return the corresponding aiida instance of class aiida.orm.Node or a
        appropriate subclass.
        """
        dbnode = DjangoNode(
            id = self.id,
            type = self.type,
            uuid = self.uuid,
            ctime = self.ctime,
            mtime = self.mtime,
            label = self.label,
            dbcomputer_id = self.dbcomputer_id,
            user_id = self.user_id,
            public = self.public,
            nodeversion = self.nodeversion
        )
        try:
            pluginclassname = from_type_to_pluginclassname(self.type)
        except DbContentError:
            raise DbContentError("The type name of node with pk= {} is "
                                 "not valid: '{}'".format(self.pk, self.type))

        try:
            PluginClass = load_plugin(Node, 'aiida.orm', pluginclassname)
        except MissingPluginError as e:
            raw_input(e)
            aiidalogger.error("Unable to find plugin for type '{}' (node= {}), "
                              "will use base Node class".format(self.type, self.pk))
            PluginClass = Node
        #~ raw_input(PluginClass)
        return PluginClass(dbnode=dbnode)

class DbCalcState(Base):
    __tablename__ = "db_dbcalcstate"

    id = Column(Integer, primary_key=True)


    dbnode = relationship('DbNode', backref=backref('dbstates', passive_deletes=True))

    state = Column(String(255))

    time = Column(DateTime(timezone=True), default=timezone.now)

    dbnode_id = Column(Integer, ForeignKey('db_dbnode.id', ondelete="CASCADE", deferrable=True, initially="DEFERRED"))
    
    __table_args__ = (
        UniqueConstraint('dbnode_id', 'state'),
    )

class DbAttribute(Base):
    __tablename__ = "db_dbattribute"
    id  = Column(Integer, primary_key = True)
    dbnode_id = Column(Integer, ForeignKey('db_dbnode.id'))
    key = Column(String(255))
    datatype = Column(String(10))
    tval = Column(String, default='')
    fval = Column(Float, default=None, nullable=True)
    ival = Column(Integer, default=None, nullable=True)
    bval = Column(Boolean, default=None, nullable=True)
    #~ dval = m.DateTimeField(default=None, null=True)
    dval = Column(DateTime, default=None, nullable = True)

class DbComputer(Base):
    __tablename__ = "db_dbcomputer"

    id = Column(Integer, primary_key=True)

    uuid = Column(UUID(as_uuid=True), default=uuid_func)
    name = Column(String(255), unique=True, nullable=False)
    hostname = Column(String(255))

    description = Column(Text, nullable=True)
    enabled = Column(Boolean)

    transport_type = Column(String(255))
    scheduler_type = Column(String(255))

    transport_params = Column(String(255))

class DbUser(Base):
    __tablename__ = "db_dbuser"

    id = Column(Integer, primary_key=True)
    email = Column(String(254), unique=True, index=True)
    password = Column(String(128))  # Clear text password ?
    first_name = Column(String(254), nullable=True)
    last_name = Column(String(254), nullable=True)
    institution = Column(String(254), nullable=True)

    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    last_login = Column(DateTime(timezone=True), default=timezone.now)
    date_joined = Column(DateTime(timezone=True), default=timezone.now)

config = get_profile_config(settings.AIIDADB_PROFILE)
engine_url = ("postgresql://{AIIDADB_USER}:{AIIDADB_PASS}@"
              "{AIIDADB_HOST}:{AIIDADB_PORT}/{AIIDADB_NAME}").format(**config)
engine = create_engine(engine_url)
Session = sessionmaker(bind=engine)

session = Session()

#~ print session.query(DbAttribute.id, DbAttribute.ival).limit(3).all()
#~ print session.query(DbComputer).all()
#~ print session.query(DbUser).all()
#~ attrs =  session.query(DbNode).filter(DbNode.attributes.any(DbAttribute.key.like('%kinds'))).first().attributes
#~ for attr in attrs:
    #~ print attr.key
