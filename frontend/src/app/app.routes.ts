import { Routes } from '@angular/router';
import { NodeViewComponent } from './nodes/node-view/node-view.component';
import { NodesTableComponent } from './nodes/nodes-table/nodes-table.component';

export const routes: Routes = [
    { path: '', redirectTo: 'nodes', pathMatch: 'full' },
    { path: 'nodes', component: NodesTableComponent },
    { path: 'nodes/:ip', component: NodeViewComponent }
];
