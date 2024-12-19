# Security Groups to CloudFormation Template Generator

This script generates a CloudFormation template for all security groups in a specified VPC. It uses AWS SDK for Python (boto3) to fetch the security groups and outputs the result in YAML format.

## Features
- Fetches all security groups associated with a specified VPC.
- Converts security group configurations into a CloudFormation-compatible YAML template.
- Handles ingress rules, including IP ranges, ports, and protocols.
- Provides warnings if no security groups are found for the specified VPC.

---

## Prerequisites

1. **Python**: Ensure Python 3.6 or higher is installed.
2. **AWS CLI Configuration**:
   - Ensure the AWS CLI is configured with appropriate credentials and permissions.
   - The IAM user or role must have `ec2:DescribeSecurityGroups` permission.
3. **Dependencies**:
   - Install the required Python libraries using:
     ```bash
     pip install boto3 pyyaml
     ```

---

## Usage

### Command-Line Arguments
The script requires two arguments:
- `region`: The AWS region where the VPC is located.
- `vpc_id`: The ID of the VPC whose security groups are to be exported.

### Example

Run the script with:
```bash
python script.py <region> <VPC_ID>
```

Example:
```bash
python script.py us-east-1 vpc-0abcd1234efgh5678
```

If no security groups are found for the specified VPC, the script will display a warning and exit.

---

## Output

- The script generates a CloudFormation template in YAML format.
- The output file is named `security_groups_<VPC_ID>.yaml`.
- Example output location:
  ```
  security_groups_vpc-0abcd1234efgh5678.yaml
  ```

---

## CloudFormation Template Structure
The generated YAML file includes:
- **Resources**: Each security group is represented as an `AWS::EC2::SecurityGroup` resource.
- **Properties**:
  - `GroupDescription`
  - `VpcId`
  - `SecurityGroupIngress` rules (including `CidrIp`, `FromPort`, `ToPort`, `IpProtocol`).

---

## Example Output

### Input VPC Information
Assume the VPC contains a security group with the following rule:
- Description: "Web server security group"
- Ingress: Allow TCP traffic from `0.0.0.0/0` on port `80`.

### Generated YAML Output
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  sg-0abcd1234efgh5678:
    Type: "AWS::EC2::SecurityGroup"
    Properties:
      GroupDescription: "Web server security group"
      VpcId: "vpc-0abcd1234efgh5678"
      SecurityGroupIngress:
        - CidrIp: "0.0.0.0/0"
          FromPort: 80
          ToPort: 80
          IpProtocol: "tcp"
```

---

## Error Handling
- If no security groups are found, a warning is displayed:
  ```plaintext
  Warning: No security groups found for VPC ID vpc-0abcd1234efgh5678 in region us-east-1.
  ```
- If required arguments are not provided, the script exits with usage instructions.

---

## License
This project is licensed under the MIT License.

---

## Contribution
Feel free to fork the repository, submit issues, or make pull requests to improve this project.

