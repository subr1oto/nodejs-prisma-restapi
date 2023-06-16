import { Router } from "express";
import { prisma } from '../db.js';

const router = Router();

router.get('/products', async (req,res) => {
    const products = await prisma.product.findMany();
    res.json(products);
});

router.get('/products/:id', async (req,res) => {
    const productFound = await prisma.product.findFirst({
        where: {
            id: parseInt(req.params.id)
        }
    })
    if (!productFound) {
        return res.status(404).json({error: "Product not found"});
    }
    
    return res.json(productFound);
})

router.post('/products', async (req, res) => {
    const newProduct = await prisma.product.create({
        data: req.body
    });
    res.json(newProduct);
});

export default router;