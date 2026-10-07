/* restrict-af-unix: equivalent of systemd's RestrictAddressFamilies=~AF_UNIX
 * (as used in leanprover/comparator README's systemd-run launch line) for hosts
 * without a systemd user manager. Installs a seccomp-BPF filter that makes
 * socket(2) with domain AF_UNIX fail with EAFNOSUPPORT (same errno systemd uses),
 * rejects non-native (x32 / i386) syscall ABIs, sets NO_NEW_PRIVS, then execs argv[1..].
 * The filter is inherited by all descendants and cannot be removed. */
#define _GNU_SOURCE
#include <stddef.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <sys/socket.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/audit.h>

#define X32_SYSCALL_BIT 0x40000000

int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: %s cmd [args...]\n", argv[0]); return 2; }
  struct sock_filter f[] = {
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
    BPF_JUMP(BPF_JMP | BPF_JGE | BPF_K, X32_SYSCALL_BIT, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (ENOSYS & SECCOMP_RET_DATA)),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_socket, 0, 3),
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[0])),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AF_UNIX, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (EAFNOSUPPORT & SECCOMP_RET_DATA)),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
  };
  struct sock_fprog prog = { .len = sizeof(f)/sizeof(f[0]), .filter = f };
  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) { perror("prctl(NO_NEW_PRIVS)"); return 111; }
  if (syscall(__NR_seccomp, SECCOMP_SET_MODE_FILTER, SECCOMP_FILTER_FLAG_TSYNC, &prog)) { perror("seccomp"); return 111; }
  execvp(argv[1], argv + 1);
  perror("execvp");
  return 127;
}
