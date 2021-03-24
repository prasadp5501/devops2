import oci
import re
import sys
from oci import util as ociutil
config = oci.config.from_file("/var/lib/jenkins/.oci/config")


def geninitscript(tag,port):

    fileout = open("initscript.sh","w")
    init_str = "#!/bin/bash\n" \
               "yum install -y java\n" \
               "wget -O /etc/yum.repos.d/public-yum-ol7.repo http://yum.oracle.com/public-yum-ol7.repo\n" \
               "yum-config-manager --enable public-yum-ol7\n" \
               "yum install -y docker-engine\n" \
               "sytemctl enable docker\n" \
               "systemctl start docker\n" \
               "echo '-Bi_Y[x#}j]4sRXA5qKZ' | docker login iad.ocir.io --username biascorpoci/prasadpatil --password-stdin\n" \
                "if [ $? -eq 0 ]\n then\n echo 'Docker login succeded' >> /tmp/docker_login.status\n " \
               "docker pull iad.ocir.io/biascorpoci/devopstest2:"+tag+"\n image_id=`sudo docker images --format '{{.ID}}'`\n " \
               "sudo docker run -P $image_id\nelse\necho 'Docker login failed' >> /tmp/docker_login.status\n fi"
    fileout.write(init_str)
    fileout.close()

def Deployinstance(tag):
    CoreClient = oci.core.ComputeClient(config)
    metadata = {}
    metadata['user_data'] = ociutil.file_content_as_launch_instance_user_data(
        "initscript.sh")
    metadata[
        'ssh_authorized_keys'] = "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAqA/v5ppQELOFtUUB5j9u0anYAaDccZPP/OywHN77/7i1rXLsIpORqIvO7oovOVtRWm/fh5Mk6RJrmWgw2PPEM4pd2R2ZA6mQkEkR/XsRLJW8A76Qt/1nhKIfCKb+X42FggEgxr0DzI00s1PUqQjCwHXjLrWX7dWJ3C4FF3mGXOgh8moQsnforKOP9PLd9n5F+T1QPG8NEYB/rm+tm53l8F1/CbGrbFsuZwK3ZUXTMX9584MVYbeiNCERLhV01Lpdn78cU/DD/qJs+l2imvktNx5oHMeS7No/mHYn+m08TVKGbx6v61tJDa6um0XahSiImmJmsvgk8FmBuexwKHY8Lw== opc"
    response_compute_client = CoreClient.launch_instance(
        launch_instance_details=oci.core.models.LaunchInstanceDetails(
            availability_domain="Vquz:US-ASHBURN-AD-1",
            compartment_id="ocid1.compartment.oc1..aaaaaaaa54qq3iezggh5d4mvqziws7mv5pf3pczjj62tvk2zgdk3r6vbzyjq",
            shape="VM.Standard2.1",
            create_vnic_details=oci.core.models.CreateVnicDetails(
                assign_public_ip=True,
                subnet_id="ocid1.subnet.oc1.iad.aaaaaaaaj44xtau4wdly2k3w3z4q2jd7zvhf7nahgi2nsi7o3lzlhannw4aa"),
            display_name=str("Devops-POC" + sys.argv[1]),
            hostname_label=str("Devops-POC" + sys.argv[1]),
            image_id="ocid1.image.oc1.iad.aaaaaaaapulaxjedwo2y3koeli6zq6evql6rropyxpni3wu44i2rbffgxgza",
            metadata=metadata,
            subnet_id="ocid1.subnet.oc1.iad.aaaaaaaaj44xtau4wdly2k3w3z4q2jd7zvhf7nahgi2nsi7o3lzlhannw4aa"
        )
    )

    print(response_compute_client.data)

if __name__ == '__main__':
    config = oci.config.from_file("/var/lib/jenkins/.oci/config")
    pattern = "EXPOSE"
    file = open("Dockerfile", "r")
    for line in file:
        if re.search(pattern, line):
            exposed_port = str(line.split(" ")[1])

    geninitscript(sys.argv[1],exposed_port)
    Deployinstance(sys.argv[1])

