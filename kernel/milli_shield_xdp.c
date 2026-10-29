#include "vmlinux.h"
#include <bpf/bpf_helpers.h>

SEC("xdp")
int milli_shield_inspect(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;

    if (eth->h_proto == __builtin_bswap16(0x0800)) { // IPv4
        struct iphdr *iph = (struct iphdr *)(eth + 1);
        if ((void *)(iph + 1) > data_end)
            return XDP_PASS;
    }

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";