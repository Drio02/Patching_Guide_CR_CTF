const express = require('express');
const router = express.Router();
const Invoice = require('../models/Invoice');


router.get('/api/invoices/:invoiceId', authMiddleware, async (req, res) => {
     try {
        // La consulta incluye el ownerId de la sesión como filtro obligatorio.
        // Si la factura no pertenece al usuario, findOne devuelve null
        const invoice = await Invoice.findOne({
            _id: req.params.invoiceId,
            ownerId: req.user.id   // se obtiene del token/sesión verificada
        });

        if (!invoice) {
            return res.status(404).json({ error: 'Invoice not found' });
        }

        return res.json(invoice);
    } catch (err) {
        return res.status(500).json({ error: 'Server error' });
    }
});