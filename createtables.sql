/* Project */
CREATE TABLE project (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 name VARCHAR(255) NOT NULL,
 title VARCHAR(255),
 beginning DATE,
 ending DATE,
 phase INT,
 introduction TEXT,
 cause TEXT,
 descriptions TEXT,
 created TIMESTAMP WITH TIME ZONE,
 created_by VARCHAR(255),
 faceimage BYTEA
);
COMMENT ON TABLE public.project IS
'This table defines generic information about the survey project.';
COMMENT ON COLUMN public.project.id IS
'This attribute defines identifer of the project, which is used in DBMS.
This identifier is mainly used in sorting entries.';
COMMENT ON COLUMN public.project.uuid IS
'This attribute defines global unique id of the project.
This unique id is used for identifying each project globaly, and it enables
to merge different projects.';
COMMENT ON COLUMN public.project.name IS 
'This attribute defines the name of the project.';
COMMENT ON COLUMN public.project.title IS 
'This attribute defines the title of the project.';
COMMENT ON COLUMN public.project.beginning IS 
'This attribute defines the date of the project beginning.';
COMMENT ON COLUMN public.project.ending IS 
'This attribute defines the date of the project ending.';
COMMENT ON COLUMN public.project.phase IS 
'This attribute defines the phase of the project.';
COMMENT ON COLUMN public.project.introduction IS 
'This attribute can be used for introducing this survey in the report.';
COMMENT ON COLUMN public.project.descriptions IS 
'This attribute can be used for describing additional information about the project.';

/* SurveyReport */
CREATE TABLE report (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 prj_id VARCHAR(36) NOT NULL REFERENCES project(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 title VARCHAR(255),
 volume VARCHAR(255),
 edition VARCHAR(255),
 series VARCHAR(255),
 publisher VARCHAR(255),
 year date,
 descriptions TEXT
);
COMMENT ON TABLE public.report IS
'This table defines information about the survey report.
This table includes general citation information.';

/* Organization */
CREATE TABLE organization (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 name VARCHAR(255) NOT NULL,
 section VARCHAR(255),
 country VARCHAR(255),
 administrativearea VARCHAR(255),
 city VARCHAR(255),
 contact_address VARCHAR(255),
 zipcode VARCHAR(255),
 phone VARCHAR(255)
);
COMMENT ON TABLE public.organization IS 'This table defines generic information about a organization.';
COMMENT ON COLUMN public.organization.id IS 'This attribute defines identifer of the organization, which is used in DBMS.';
COMMENT ON COLUMN public.organization.uuid IS 'This attribute defines global unique id of the organization.';
COMMENT ON COLUMN public.organization.name IS 'This attribute defines the name of the organization.';
COMMENT ON COLUMN public.organization.section IS 'This attribute defines the section name of the organization.';
COMMENT ON COLUMN public.organization.country IS 'This attribute defines the country where the organization located. Defined by CI_Contact.';
COMMENT ON COLUMN public.organization.administrativearea IS 'This attribute defines the administrative area where the organization located. Defined by CI_Contact.';
COMMENT ON COLUMN public.organization.city IS 'This attribute defines the city where the organization located. Defined by CI_Contact.';
COMMENT ON COLUMN public.organization.contact_address IS 'This attribute defines the contact address where the organization located. Defined by CI_Contact.';
COMMENT ON COLUMN public.organization.zipcode IS 'This attribute defines the zip code where the organization located. Defined by CI_Contact..';
COMMENT ON COLUMN public.organization.phone IS 'This attribute defines the phone number of the organization. Defined by CI_Contact.';

/* Member */
CREATE TABLE member (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 org_id VARCHAR(36) NOT NULL REFERENCES organization(uuid) ON UPDATE CASCADE ON DELETE SET NULL,
 avatar BYTEA,
 surname VARCHAR(255),
 firstname VARCHAR(255),
 birthday DATE,
 country VARCHAR(255),
 administrativearea VARCHAR(255),
 city VARCHAR(255),
 contact_address VARCHAR(255),
 zipcode VARCHAR(255),
 email VARCHAR(255),
 phone VARCHAR(255),
 mobile_phone VARCHAR(255),
 apointment VARCHAR(255),
 username VARCHAR(255) NOT NULL UNIQUE,
 password VARCHAR(255) NOT NULL,
 usertype VARCHAR(255) NOT NULL
);
COMMENT ON TABLE public.member IS 'This table defines generic information about a member.';
COMMENT ON COLUMN public.member.id IS 'This attribute defines identifer of the organization, which is used in DBMS.';
COMMENT ON COLUMN public.member.uuid IS 'This attribute defines global unique id of the organization.';
COMMENT ON COLUMN public.member.country IS 'This attribute defines the country where the member living. Defined by CI_Contact.';
COMMENT ON COLUMN public.member.administrativearea IS 'This attribute defines the administrative area where the memver living. Defined by CI_Contact.';
COMMENT ON COLUMN public.member.city IS 'This attribute defines the city where the member living. Defined by CI_Contact.';
COMMENT ON COLUMN public.member.contact_address IS 'This attribute defines the contact address where the member living. Defined by CI_Contact.';
COMMENT ON COLUMN public.member.zipcode IS 'This attribute defines the zip code of the address. Defined by CI_Contact..';
COMMENT ON COLUMN public.member.phone IS 'This attribute defines the phone number of the member. Defined by CI_Contact.';
COMMENT ON COLUMN public.member.username IS 'This attribute defines the acount name of the member on the archiving system.';
COMMENT ON COLUMN public.member.password IS 'This attribute defines the member password for the archiving system.';
COMMENT ON COLUMN public.member.usertype IS 'This attribute defines the member types for the archiving system.';

/* Member role in the project */
CREATE TABLE role (
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 prj_id VARCHAR(36) NOT NULL REFERENCES project(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 mem_id VARCHAR(36) NOT NULL REFERENCES member(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 beginning DATE,
 ending DATE,
 rolename VARCHAR(255),
 biography TEXT
);

CREATE TABLE section (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 rep_id VARCHAR(36) NOT NULL REFERENCES report(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 order_number INT,
 section_name VARCHAR(255),
 written_by VARCHAR(255),
 created_by VARCHAR(36) NOT NULL,
 modified_by VARCHAR(36) NOT NULL,
 date_created TIMESTAMP WITH TIME ZONE,
 date_modified TIMESTAMP WITH TIME ZONE,
 body TEXT
);
COMMENT ON TABLE public.section IS
'This table defines sections of the survey report.
Any kinds of explainations are denoted in this section.';

CREATE TABLE surveydiary (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 prj_id VARCHAR(36) NOT NULL REFERENCES project(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 mem_id VARCHAR(36) NOT NULL REFERENCES member(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 date_created TIMESTAMP WITH TIME ZONE,
 date_modified TIMESTAMP WITH TIME ZONE,
 weather VARCHAR(255),
 tempurature REAL,
 humidity REAL,
 body TEXT
);

/* Consolidation */
CREATE TABLE consolidation (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 prj_id VARCHAR(36) NOT NULL REFERENCES project(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 name VARCHAR(255),
 faceimage BYTEA,
 geographic_name VARCHAR(255),
 geographic_extent geometry(MultiPolygon,4612),
 represented_point geometry(Point,4612),
 estimated_area geometry(MultiPolygon,4612),
 estimated_period_beginning VARCHAR(255),
 estimated_period_ending VARCHAR(255),
 descriptions TEXT
);

/* Material */
CREATE TABLE material (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 con_id VARCHAR(36) NOT NULL REFERENCES consolidation(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 name VARCHAR(255),
 estimated_period_beginning VARCHAR(255),
 estimated_period_ending VARCHAR(255),
 represented_point geometry(Point,4612),
 path geometry(MultiLineStringM,4612),
 area geometry(Polygon,4612),
 material_number VARCHAR(255),
 descriptions TEXT
);

CREATE TABLE digitized_image (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 prj_id VARCHAR(36) REFERENCES project(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 rep_id VARCHAR(36) REFERENCES report(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 sec_id VARCHAR(36) REFERENCES section(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 con_id VARCHAR(36) REFERENCES consolidation(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 mat_id VARCHAR(36) REFERENCES material(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 filename		varchar,
 image			bytea,
 thumbnail		bytea,
 descriptions VARCHAR(255),
 exif_orientation	varchar,
 exif_version		varchar,
 exif_imagewidth		integer,
 exif_imageheight	integer,
 exif_datetimeoriginal	timestamp,
 exif_datetimedigitized	timestamp,
 exif_datetime		timestamp,
 exif_make		varchar,
 exif_model		varchar,
 exif_fnumber		double precision,
 exif_focallength	double precision,
 exif_isospeedratings	integer,
 exif_exposuretime	varchar,
 exif_maxaperturevalue	double precision,
 exif_flash		varchar,
 exif_meteringmode	varchar,
 exif_lightsource	varchar,
 exif_exposureprogram	varchar,
 exif_colorspace		varchar,
 exif_ycbcrpositioning	varchar,
 exif_compesedbitsperpixel	 double precision,
 exif_xresolution	integer,
 exif_yresolution	integer,
 exif_resolutionunit	varchar,
 exif_gps_datestamp	timestamp,
 exif_gps_timestamp	timestamp,
 exif_gps_measuremode	varchar,
 exif_gps_mapdatum	varchar,
 exif_gps_dop		double precision,
 exif_gps_status		varchar,
 exif_gps_latitude	double precision,
 exif_gps_latituderef	varchar,
 exif_gps_longitude	double precision,
 exif_gps_longituderef	varchar,
 exif_gps_altitude	double precision,
 exif_gps_altituderef	varchar,
 exif_gps_imgdirection	double precision,
 exif_gps_imgdirectionref	varchar,
 exif_gps_speed		double precision,
 exif_gps_track		varchar,
 exif_gps_trackref	varchar,
 exif_gps_speedref	varchar,
 exif_gps_differential	varchar
);

CREATE TABLE additional_information (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 prj_id VARCHAR(36) REFERENCES project(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 con_id VARCHAR(36) REFERENCES consolidation(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 mat_id VARCHAR(36) REFERENCES material(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 key VARCHAR(255),
 value VARCHAR(255),
 type VARCHAR(50)
);
COMMENT ON TABLE public.additional_information IS 
'This table defines additional information.
Users can define specific attributes freely.';
COMMENT ON COLUMN public.additional_information.key IS 
'This column defines the name of the entry.';
COMMENT ON COLUMN public.additional_information.value IS 
'This column defines the value of the entry.';
COMMENT ON COLUMN public.additional_information.type IS 
'This column defines the data type for this entry to cast data types.';


/*==== Relationships between tables ====*/
/* Consolidation of Consolidation*/
CREATE TABLE consolidation_of_consolidation (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 parent VARCHAR(36) NOT NULL REFERENCES consolidation(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 child VARCHAR(36) NOT NULL REFERENCES consolidation(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 descriptions TEXT
);

/* Material of Material */
CREATE TABLE material_to_material (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 relating_from VARCHAR(36) NOT NULL REFERENCES material(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 relating_to VARCHAR(36) NOT NULL REFERENCES material(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 relation_type VARCHAR(255),
 descriptions VARCHAR(255)
);

/* Figures in articles */
CREATE TABLE figure (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 sec_id VARCHAR(36) REFERENCES section(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 dir_id VARCHAR(36) REFERENCES surveydiary(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 img_id VARCHAR(36) NOT NULL REFERENCES digitized_image(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 label VARCHAR(10),
 number VARCHAR(10),
 description TEXT
);


CREATE TABLE file (
 id SERIAL NOT NULL,
 uuid VARCHAR(36) NOT NULL PRIMARY KEY,
 prj_id VARCHAR(36) REFERENCES project(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 con_id VARCHAR(36) REFERENCES consolidation(uuid) ON UPDATE CASCADE ON DELETE CASCADE,
 mat_id VARCHAR(36) REFERENCES material(uuid) ON UPDATE CASCADE ON DELETE CASCADE,

 registered_by INT,

 srf_id VARCHAR(255) NOT NULL,
 sub_id INT NOT NULL,
 file_path VARCHAR(255),
 file_name VARCHAR(255),
 mimetype VARCHAR(255)
);


/* 
CREATE TABLE surface (
 surfaceid VARCHAR(255) NOT NULL,
 materialid INT NOT NULL,
 consolidationid INT NOT NULL,
 projectid INT NOT NULL,
 geometric_space BYTEA
);

ALTER TABLE surface ADD CONSTRAINT PK_surface PRIMARY KEY (surfaceid,materialid,consolidationid,projectid);

CREATE TABLE equipments (
 equipmentsid INT NOT NULL,
 projectid INT NOT NULL,
 related_equipments INT,
 name VARCHAR(255),
 type_of_equipments VARCHAR(255),
 maker VARCHAR(255),
 model VARCHAR(255),
 serialnumber VARCHAR(255)
);

ALTER TABLE equipments ADD CONSTRAINT PK_equipments PRIMARY KEY (equipmentsid,projectid);


CREATE TABLE keywords (
 keywordsid INT NOT NULL,
 materialid INT NOT NULL,
 consolidationid INT NOT NULL,
 projectid INT NOT NULL,
 keyword VARCHAR(255)
);

ALTER TABLE keywords ADD CONSTRAINT PK_keywords PRIMARY KEY (keywordsid,materialid,consolidationid,projectid);


CREATE TABLE Subject (
 subjectid INT NOT NULL,
 surfaceid VARCHAR(255) NOT NULL,
 materialid INT NOT NULL,
 consolidationid INT NOT NULL,
 projectid INT NOT NULL,
 object_name VARCHAR(255),
 arrangement geometry(Polygon,4612),
 descriptions TEXT
);

ALTER TABLE Subject ADD CONSTRAINT PK_Subject PRIMARY KEY (subjectid,surfaceid,materialid,consolidationid,projectid);

CREATE TABLE device_specification (
 specid INT NOT NULL,
 equipmentsid INT NOT NULL,
 projectid INT NOT NULL,
 item VARCHAR(255),
 value VARCHAR(255)
);

ALTER TABLE device_specification ADD CONSTRAINT PK_device_specification PRIMARY KEY (specid,equipmentsid,projectid);
 */
