from sqlalchemy import Table, Column, create_engine
from sqlalchemy import Integer, ForeignKey, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation

#engine = create_engine("sqlite:///skeletons.db", echo=False)
Base = declarative_base()
metadata = Base.metadata


class olvSkeleton(object):
    """
        Skeleton model for ObjectListView
    """

    def __init__(self, data):
        self.skeleton_id = data['skeleton_id']  # unique row id from database
        self.site = data['site']
        self.location = data['location']
        self.skeleton = data['skeleton']
        self.obs_date = data['obs_date']
        self.observer = data['observer']


class Skeleton(Base):
    """
        Skeleton - comment
    """
    __tablename__ = "skeleton"

    skeleton_id = Column(Integer, primary_key=True, autoincrement=True)
    site = Column("site", String(50))
    location = Column("location", String(50))
    skeleton = Column("skeleton", String(50))
    obs_date = Column("obs_date", String(10))
    observer = Column("observer", String(50))
    skeleton_description = Column("skeleton_description", String(255))

    # skull
    frontal = Column(Integer)
    parietal_l = Column(Integer)
    parietal_r = Column(Integer)
    occipital = Column(Integer)
    temporal_l = Column(Integer)
    temporal_r = Column(Integer)
    sphenoid = Column(Integer)
    nasal_l = Column(Integer)
    nasal_r = Column(Integer)
    maxilla_l = Column(Integer)
    maxilla_r = Column(Integer)
    zygomatic_l = Column(Integer)
    zygomatic_r = Column(Integer)
    mandible = Column(Integer)
    palatine_l = Column(Integer)
    palatine_r = Column(Integer)
    lacrimal_l = Column(Integer)
    lacrimal_r = Column(Integer)
    orbit_l = Column(Integer)
    orbit_r = Column(Integer)
    ethmoid = Column(Integer)
    thyroid = Column(Integer)
    hyoid = Column(Integer)
    calotte = Column(Integer)

    ilium_l = Column(Integer)
    ilium_r = Column(Integer)
    scapula_l = Column(Integer)
    scapula_r = Column(Integer)
    manubrium = Column(Integer)
    ischium_l = Column(Integer)
    ischium_r = Column(Integer)
    patella_l = Column(Integer)
    patella_r = Column(Integer)
    c_sterni = Column(Integer)
    pubic_l = Column(Integer)
    pubic_r = Column(Integer)
    x_process = Column(Integer)
    sacrum = Column(Integer)
    coccyx = Column(Integer)

    clavicle_l_djs = Column(Integer)
    clavicle_l_d13 = Column(Integer)
    clavicle_l_m13 = Column(Integer)
    clavicle_l_p13 = Column(Integer)
    clavicle_l_pjs = Column(Integer)
    clavicle_r_djs = Column(Integer)
    clavicle_r_d13 = Column(Integer)
    clavicle_r_m13 = Column(Integer)
    clavicle_r_p13 = Column(Integer)
    clavicle_r_pjs = Column(Integer)

    humerus_l_djs = Column(Integer)
    humerus_l_d13 = Column(Integer)
    humerus_l_m13 = Column(Integer)
    humerus_l_p13 = Column(Integer)
    humerus_l_pjs = Column(Integer)
    humerus_r_djs = Column(Integer)
    humerus_r_d13 = Column(Integer)
    humerus_r_m13 = Column(Integer)
    humerus_r_p13 = Column(Integer)
    humerus_r_pjs = Column(Integer)

    radius_l_djs = Column(Integer)
    radius_l_d13 = Column(Integer)
    radius_l_m13 = Column(Integer)
    radius_l_p13 = Column(Integer)
    radius_l_pjs = Column(Integer)
    radius_r_djs = Column(Integer)
    radius_r_d13 = Column(Integer)
    radius_r_m13 = Column(Integer)
    radius_r_p13 = Column(Integer)
    radius_r_pjs = Column(Integer)

    ulna_l_djs = Column(Integer)
    ulna_l_d13 = Column(Integer)
    ulna_l_m13 = Column(Integer)
    ulna_l_p13 = Column(Integer)
    ulna_l_pjs = Column(Integer)
    ulna_r_djs = Column(Integer)
    ulna_r_d13 = Column(Integer)
    ulna_r_m13 = Column(Integer)
    ulna_r_p13 = Column(Integer)
    ulna_r_pjs = Column(Integer)

    femur_l_djs = Column(Integer)
    femur_l_d13 = Column(Integer)
    femur_l_m13 = Column(Integer)
    femur_l_p13 = Column(Integer)
    femur_l_pjs = Column(Integer)
    femur_r_djs = Column(Integer)
    femur_r_d13 = Column(Integer)
    femur_r_m13 = Column(Integer)
    femur_r_p13 = Column(Integer)
    femur_r_pjs = Column(Integer)

    tibia_l_djs = Column(Integer)
    tibia_l_d13 = Column(Integer)
    tibia_l_m13 = Column(Integer)
    tibia_l_p13 = Column(Integer)
    tibia_l_pjs = Column(Integer)
    tibia_r_djs = Column(Integer)
    tibia_r_d13 = Column(Integer)
    tibia_r_m13 = Column(Integer)
    tibia_r_p13 = Column(Integer)
    tibia_r_pjs = Column(Integer)

    fibula_l_djs = Column(Integer)
    fibula_l_d13 = Column(Integer)
    fibula_l_m13 = Column(Integer)
    fibula_l_p13 = Column(Integer)
    fibula_l_pjs = Column(Integer)
    fibula_r_djs = Column(Integer)
    fibula_r_d13 = Column(Integer)
    fibula_r_m13 = Column(Integer)
    fibula_r_p13 = Column(Integer)
    fibula_r_pjs = Column(Integer)

    metacarpals_l_1 = Column(Integer)
    metacarpals_l_2 = Column(Integer)
    metacarpals_l_3 = Column(Integer)
    metacarpals_l_4 = Column(Integer)
    metacarpals_l_5 = Column(Integer)
    metacarpals_r_1 = Column(Integer)
    metacarpals_r_2 = Column(Integer)
    metacarpals_r_3 = Column(Integer)
    metacarpals_r_4 = Column(Integer)
    metacarpals_r_5 = Column(Integer)

    metatarsals_l_1 = Column(Integer)
    metatarsals_l_2 = Column(Integer)
    metatarsals_l_3 = Column(Integer)
    metatarsals_l_4 = Column(Integer)
    metatarsals_l_5 = Column(Integer)
    metatarsals_r_1 = Column(Integer)
    metatarsals_r_2 = Column(Integer)
    metatarsals_r_3 = Column(Integer)
    metatarsals_r_4 = Column(Integer)
    metatarsals_r_5 = Column(Integer)

    vertebrae_c_1 = Column(Integer)
    vertebrae_c_2 = Column(Integer)
    vertebrae_c_3 = Column(Integer)
    vertebrae_c_4 = Column(Integer)
    vertebrae_c_5 = Column(Integer)
    vertebrae_t_1 = Column(Integer)
    vertebrae_t_2 = Column(Integer)
    vertebrae_t_3 = Column(Integer)
    vertebrae_t_4 = Column(Integer)
    vertebrae_t_5 = Column(Integer)
    vertebrae_l_1 = Column(Integer)
    vertebrae_l_2 = Column(Integer)
    vertebrae_l_3 = Column(Integer)
    vertebrae_l_4 = Column(Integer)
    vertebrae_l_5 = Column(Integer)
    vertebrae_remarks = Column("vertebrae_remarks", String(100))

    ribs_l_whole = Column(Integer)
    ribs_l_send = Column(Integer)
    ribs_l_vend = Column(Integer)
    ribs_l_frag = Column(Integer)
    ribs_r_whole = Column(Integer)
    ribs_r_send = Column(Integer)
    ribs_r_vend = Column(Integer)
    ribs_r_frag = Column(Integer)
    ribs_u_whole = Column(Integer)
    ribs_u_send = Column(Integer)
    ribs_u_vend = Column(Integer)
    ribs_u_frag = Column(Integer)

    phalanges_hand_p = Column(Integer)
    phalanges_hand_m = Column(Integer)
    phalanges_hand_d = Column(Integer)
    phalanges_foot_p = Column(Integer)
    phalanges_foot_m = Column(Integer)
    phalanges_foot_d = Column(Integer)

    scaphoid_l = Column(Integer)
    scaphoid_r = Column(Integer)
    lunate_l = Column(Integer)
    lunate_r = Column(Integer)
    triquetral_l = Column(Integer)
    triquetral_r = Column(Integer)
    pisiform_l = Column(Integer)
    pisiform_r = Column(Integer)
    trapezium_l = Column(Integer)
    trapezium_r = Column(Integer)
    trapezoid_l = Column(Integer)
    trapezoid_r = Column(Integer)
    capitate_l = Column(Integer)
    capitate_r = Column(Integer)
    hamate_l = Column(Integer)
    hamate_r = Column(Integer)
    sesamoids_hand = Column(Integer)

    talus_l = Column(Integer)
    talus_r = Column(Integer)
    calcaneus_l = Column(Integer)
    calcaneus_r = Column(Integer)
    cun_1_l = Column(Integer)
    cun_1_r = Column(Integer)
    cun_2_l = Column(Integer)
    cun_2_r = Column(Integer)
    cun_3_l = Column(Integer)
    cun_3_r = Column(Integer)
    navicular_l = Column(Integer)
    navicular_r = Column(Integer)
    cuboid_l = Column(Integer)
    cuboid_r = Column(Integer)
    sesamoids_foot = Column(Integer)

    def __repr__(self):
        """
            __repr - comment
        """
        return "Skeleton: {}, {} - {}".format(self.site, self.location, self.skeleton)



