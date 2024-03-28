# ansible-role-vnc-server #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-vnc-server/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-vnc-server/actions)
[![CodeQL](https://github.com/cisagov/ansible-role-vnc-server/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-vnc-server/actions/workflows/codeql-analysis.yml)

An Ansible role for installing a VNC server.

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| vnc\_server\_password | The password for the VNC user. | Defaults to a random value. | No |
| vnc\_server\_private\_ssh\_key | The private ssh key for the VNC user. | By default no such key is assigned to the VNC user. | No |
| vnc\_server\_public\_ssh\_key | The public ssh key for the VNC user. | By default no such key is assigned to the VNC user. | No |
| vnc\_server\_ssh\_key\_type | The case-independent SSH key type. Valid values are the key types supported by SSH:  DSA, ECDSA, ECDSA_SK, ED25519, ED25519_SK, and RSA. | `ed25519` | No |
| vnc\_server\_username | The name of the VNC user, which will be created. | `vnc` | No |
| vnc\_server\_user\_groups | A list of additional groups to which the VNC user should belong. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |
| vnc\_server\_user\_uid | The UID to use for the VNC user. | [Omitted](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#making-variables-optional) | No |

## Dependencies ##

None.

## Installation ##

This role can be installed via the command:

```console
ansible-galaxy ansible-galaxy install --role-file path/to/requirements.yml
```

where `requirements.yml` looks like:

```yaml
---
- name: skeleton
  src: https://github.com/cisagov/skeleton-ansible-role
```

and may contain other roles as well.

For more information about installing Ansible roles via a YAML file,
please see [the `ansible-galaxy`
documentation](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-multiple-roles-from-a-file).

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install VNC server
      ansible.builtin.include_role:
        name: vnc_server
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

David Redmin - <david.redmin@gwe.cisa.dhs.gov>
