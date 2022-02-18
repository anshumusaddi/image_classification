import json
import os

xmp = '''\
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 7.0-c000 1.000000, 0000/00/00-00:00:00        ">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
    xmlns:tiff="http://ns.adobe.com/tiff/1.0/"
    xmlns:exif="http://ns.adobe.com/exif/1.0/"
    xmlns:aux="http://ns.adobe.com/exif/1.0/aux/"
    xmlns:exifEX="http://cipa.jp/exif/1.0/"
    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
    xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:crd="http://ns.adobe.com/camera-raw-defaults/1.0/"
    xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
   xmp:Rating="{rating}"
   xmp:Label="{label}">
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>\
'''

labels = ["Red", "Yellow", "Green", "Blue", "Purple"]

with open("output.json") as fp:
    input_data = json.load(fp)

for i, cluster in enumerate(input_data):
    for image_name, data in cluster.items():
        xmp_data = xmp.format(rating=data["stars"], label=labels[i % 5])
        xmp_file_name = image_name.split(".")[0] + ".xmp"
        with open(os.path.join("xmp_data", xmp_file_name), "w") as fp:
            fp.write(xmp_data)
