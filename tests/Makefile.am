#
# tests/Makefile.am
#
# For the license, see the LICENSE file in the root directory.
#

check_PROGRAMS =

TESTS = \
	test_vtpm_proxy

if WITH_CHARDEV
TESTS += \
	test_ctrlchannel2 \
	test_ctrlchannel4
endif

TESTS += \
	test_ctrlchannel \
	test_ctrlchannel3 \
	test_encrypted_state \
	test_getcap \
	test_hashing \
	test_hashing2 \
	test_init \
	test_locality \
	test_migration_key \
	test_resume_volatile \
	test_save_load_encrypted_state \
	test_save_load_state \
	test_setbuffersize \
	test_volatilestate \
	test_swtpm_bios \
	test_wrongorder

if WITH_SWTPM_SETUP
TESTS += \
	test_commandline \
	test_parameters
endif

if WITH_GNUTLS
TESTS += \
	test_swtpm_cert
if WITH_SWTPM_SETUP
TESTS += \
	test_swtpm_setup_create_cert
endif
endif

EXTRA_DIST=$(TESTS) \
	swtpm_setup.conf \
	common \
	create_certs.sh \
	data/issuercert.pem \
	data/pubek.pem \
	data/signkey.pem \
	data/keyfile.txt \
	data/pwdfile.txt \
	data/migkey1/volatilestate.bin \
	data/tpmstate1/tpm-00.permall \
	data/tpmstate1/tpm-00.volatilestate \
	data/tpmstate1/README \
	data/tpmstate2/tpm-00.permall \
	data/tpmstate2/tpm-00.volatilestate \
	data/tpmstate2/pwdfile.txt \
	data/tpmstate2/README \
	test_clientfds.py \
	test_common \
	test_cuse \
	test_setdatafd.py \
	test_swtpm_cert \
	_test_encrypted_state \
	_test_getcap \
	_test_hashing \
	_test_hashing2 \
	_test_init \
	_test_locality \
	_test_migration_key \
	_test_migration_key_2 \
	_test_resume_volatile \
	_test_save_load_encrypted_state \
	_test_save_load_state \
	_test_setbuffersize \
	_test_swtpm_bios \
	_test_volatilestate \
	_test_wrongorder

check-display:
	@if test -n "$$SWTPM_EXE"; then \
		echo "*** Using SWTPM_EXE=$$SWTPM_EXE"; \
	fi
	@if test -n "$$SWTPM_BIOS"; then \
		echo "*** Using SWTPM_BIOS=$$SWTPM_BIOS"; \
	fi
	@if test -n "$$SWTPM_IOCTL"; then \
		echo "*** Using SWTPM_IOCTL=$$SWTPM_IOCTL"; \
	fi

check: check-am check-display
