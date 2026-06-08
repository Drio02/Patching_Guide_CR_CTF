const express = require('express');
const router = express.Router();
const Invoice = require('../models/Invoice');

router.get('/api/invoices/:invoiceId', authMiddleware, async (req, res) => {
    try {
        // Se busca factura solo por su ID, sin validar que pertenezca al usuario
        const invoice = await Invoice.findById(req.params.invoideId);

        if (!invoice) {
            return res.status(404).json({ error: 'Invoice not found' });
        }

        return res.json(invoice);
    } catch (err) {
        return res.status(500).json({ error: 'Server error' });
    }
});

/* 
    Con el middleware se confirma que el usuario esta registrado, pero no que tenga derecho sobre invoiceId. 
    Se puede iterar sobre diferentes IDs y obtener datos sensibles.
*/

// ---------------------------------------------------------------------------------------------------------------------------------