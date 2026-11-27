import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { ApiService, Product } from './api.service';

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private api = inject(ApiService);

  products = signal<Product[]>([]);
  selected = signal<Product | null>(null);
  message = signal('');
  error = signal('');
  loading = signal(false);

  customerName = '';
  quantity = 1;

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.api.getProducts().subscribe({
      next: (products) => this.products.set(products),
      error: () => this.error.set('Impossible de charger les produits. Le serveur ne répond pas.'),
    });
  }

  choose(product: Product): void {
    this.selected.set(product);
    this.quantity = 1;
    this.message.set('');
    this.error.set('');
  }

  cancel(): void {
    this.selected.set(null);
  }

  order(): void {
    const product = this.selected();
    if (!product) return;

    this.loading.set(true);
    this.error.set('');
    this.message.set('');

    this.api
      .createOrder({
        customer_name: this.customerName,
        product_id: product.id,
        quantity: this.quantity,
      })
      .subscribe({
        next: (order) => {
          this.message.set(
            `Merci ${order.customer_name} ! Commande n°${order.id} enregistrée : ${this.fcfa(order.total)}.`
          );
          this.selected.set(null);
          this.customerName = '';
          this.loading.set(false);
          this.loadProducts();
        },
        error: (err: HttpErrorResponse) => {
          this.error.set(this.errorText(err));
          this.loading.set(false);
        },
      });
  }

  fcfa(amount: number): string {
    return amount.toLocaleString('fr-FR') + ' FCFA';
  }

  icon(name: string): string {
    const n = name.toLowerCase();
    if (n.includes('panier')) return '🧺';
    if (n.includes('boubou')) return '👘';
    if (n.includes('sac')) return '👜';
    if (n.includes('sandale')) return '🩴';
    if (n.includes('collier')) return '📿';
    if (n.includes('statuette')) return '🗿';
    return '🎁';
  }

  private errorText(err: HttpErrorResponse): string {
    if (err.status === 400) return err.error?.detail ?? 'Stock insuffisant.';
    if (err.status === 404) return 'Ce produit n’existe plus.';
    if (err.status === 422) return 'Vérifie ton nom (2 caractères minimum) et la quantité (entre 1 et 100).';
    return 'Le serveur ne répond pas. Réessaie plus tard.';
  }
}