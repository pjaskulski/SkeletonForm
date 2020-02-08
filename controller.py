from model import Skeleton, olvSkeleton, metadata
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def add_record(session, data):
    """
    session - 
    data - dictionary {"site":"Warsaw"}
    """
    skeleton = Skeleton()
    skeleton.site = data["site"]
    skeleton.location = data["location"]
    skeleton.skeleton = data["skeleton"]
    skeleton.observer = data["observer"]
    skeleton.obs_date = data["obs_date"]
    session.add(skeleton)
    session.commit()
    return skeleton.skeleton_id


def connect_to_database(db_name):
    """
    connect to sqlite database, return a Session object
    """
    engine = create_engine("sqlite:///" + db_name, echo=False)
    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def convert_results(results):
    """
    convert results to olvSkeletons objects
    """
    skeletons = []
    for record in results:
        data = {}
        data['skeleton_id'] = record.skeleton_id
        data['site'] = record.site
        data['location'] = record.location
        data['skeleton'] = record.skeleton
        data['observer'] = record.observer
        data['obs_date'] = record.obs_date

        skeleton = olvSkeleton(data)
        skeletons.append(skeleton)

    return skeletons


def delete_record(session, id_num):
    """
    delete a record from the database
    """
    record = session.query(Skeleton).filter_by(skeleton_id=id_num).one()
    session.delete(record)
    session.flush()
    session.commit()


def edit_record(session, id_num, row):
    """ 
    Edit a record 
    row - dictionary: {"site":"Warsaw"}
    """

    record = session.query(Skeleton).filter_by(skeleton_id=id_num).one()
    record.site = row["site"]
    record.location = row["location"]
    record.skeleton = row["skeleton"]
    record.observer = row["observer"]
    record.obs_date = row["obs_date"]
    session.add(record)
    session.flush()
    session.commit()


def get_all_records(session):
    """
    return all records
    """
    result = session.query(Skeleton).all()
    skeletons = convert_results(result)
    return skeletons


def search_records(session, filter_choice, keyword):
    """
    Searches the database based on the filter chosen and the keyword
    given by the user
    """
    if filter_choice == "Site":
        qry = session.query(Skeleton)
        result = qry.filter(Skeleton.site.contains('%s' % keyword)).all()
    elif filter_choice == "Location":
        qry = session.query(Skeleton)
        result = qry.filter(Skeleton.location.contains('%s' % keyword)).all()
    elif filter_choice == "Skeleton":
        qry = session.query(Skeleton)
        result = qry.filter(Skeleton.skeleton.contains('%s' % keyword)).all()
    elif filter_choice == "Observer":
        qry = session.query(Skeleton)
        result = qry.filter(Skeleton.observer.contains('%s' % keyword)).all()

    skeletons = convert_results(result)

    return skeletons


def find_skeleton(session, skeleton_id):
    """ find_skeleton """
    result = session.query(Skeleton).get(skeleton_id)

    return result


def edit_preservation(session, id_num, data):
    """ 
    Edit a record 
    data - dictionary: {'forntal': 1}
    """

    for k, v in data.items():
        if type(v) == type(1) and v < 0:
            data[k] = None

    record = session.query(Skeleton).filter_by(skeleton_id=id_num).update(data)

    session.flush()
    session.commit()
