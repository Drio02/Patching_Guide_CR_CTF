const express = require('express');
const axios = require('axios');
const dns = require('dns').promises;
const net = require('net');
const router = express.Router();

// Rangos internos IPv4 e IPv6 (sin dependencias externas)
const blocked = new net.BlockList();
for (const [ip, prefix] of [
    ['0.0.0.0', 8], ['10.0.0.0', 8], ['100.64.0.0', 10], ['127.0.0.0', 8],
    ['169.254.0.0', 16], ['172.16.0.0', 12], ['192.168.0.0', 16], ['224.0.0.0', 4],
]) blocked.addSubnet(ip, prefix, 'ipv4');
for (const [ip, prefix] of [['::', 128], ['::1', 128], ['fc00::', 7], ['fe80::', 10], ['::ffff:0:0', 96]])
    blocked.addSubnet(ip, prefix, 'ipv6');

async function checkUrl(raw) {
    let u;
    try { u = new URL(String(raw)); } catch { return null; }
    if (!['http:', 'https:'].includes(u.protocol)) return null;
    const host = u.hostname.replace(/^\[|\]$/g, '');
    const addrs = net.isIP(host) ? [{ address: host, family: net.isIP(host) }]
                                 : await dns.lookup(host, { all: true }).catch(() => []);
    if (!addrs.length) return null;
    for (const a of addrs)
        if (blocked.check(a.address, a.family === 6 ? 'ipv6' : 'ipv4')) return null;
    return u.toString();
}

// Patch: validar IP resuelta + sin redirects + timeout
router.post('/webhook/test', async (req, res) => {
    const url = await checkUrl(req.body.url);
    if (!url) return res.sendStatus(403);
    const r = await axios.get(url, { maxRedirects: 0, timeout: 5000, validateStatus: () => true });
    res.send(r.data);
});

module.exports = router;
