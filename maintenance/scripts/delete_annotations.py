# -----------------------------------------------------------------------------
#  Copyright (C) 2018 University of Dundee. All rights reserved.
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ------------------------------------------------------------------------------

# Delete Annotations of a particular namespace from all Images in a Dataset

import argparse
from omero.gateway import BlitzGateway


def run(username, password, dataset_id, ns, host, port):

    conn = BlitzGateway(username, password, host=host, port=port)
    try:
        conn.connect()
        dataset = conn.getObject("Dataset", dataset_id)

        for image in dataset.listChildren():
            ann_ids = [a.id for a in image.listAnnotations(ns)]
            if len(ann_ids) > 0:
                print "Deleting %s annotations..." % len(ann_ids)
                conn.deleteObjects('Annotation', ann_ids)
    except Exception as exc:
            print "Error while deleting annotations: %s" % str(exc)
    finally:
        conn.close()


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('dataset_id')
    parser.add_argument('--namespace', default="omero.batch_roi_export.map_ann",
                        help="The namespace of the annotations")
    parser.add_argument('--server', default="outreach.openmicroscopy.org",
                        help="OMERO server hostname")
    parser.add_argument('--port', default=4064, help="OMERO server port")
    args = parser.parse_args(args)
    run(args.username, args.password, args.dataset_id, args.namespace,
    	args.server, args.port)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])