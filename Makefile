.PHONY: setup install

UPDATE           = yes
PIP              = .virtualenv/bin/pip
ANSIBLE_PLAYBOOK = .virtualenv/bin/ansible-playbook --extra-vars cwd="$(shell pwd)" --extra-vars update_repos="$(UPDATE)"
RM_SUDO_PASS     = rm --force .sudo_pass
ON_FAILURE       = { $(RM_SUDO_PASS) && exit 1; }

setup:
	virtualenv --python /usr/bin/python2 .virtualenv
	$(PIP) install --upgrade --requirement requirements.txt

install:
	@$(ANSIBLE_PLAYBOOK) stage1.yml || $(ON_FAILURE)
	@for repo in $$(cat .repo-names); do $(ANSIBLE_PLAYBOOK) --extra-vars dotfiles="repos/$${repo}" stage2.yml || $(ON_FAILURE); done
	@$(RM_SUDO_PASS)
