.PHONY: build install

build:
	./scripts/build_skill.sh

install:
ifneq ($(strip $(DEST)),)
	./scripts/install_skill.sh "$(DEST)"
else
	./scripts/install_skill.sh
endif
