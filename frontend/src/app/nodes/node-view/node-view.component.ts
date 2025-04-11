import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Node, NodesService } from '../nodes.service';

@Component({
    selector: 'app-node-view',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './node-view.component.html',
    styleUrl: './node-view.component.css'
})
export class NodeViewComponent implements OnInit {

    ip!: string;
    node!: Node;

    constructor(
        private route: ActivatedRoute,
        private nodeService: NodesService
    ) { }

    ngOnInit(): void {
        this.route.paramMap.subscribe(params => {
            this.ip = params.get('ip') ?? '';
            this.nodeService.getNode(this.ip).subscribe(node => {
                this.node = node;
            });
        });
    }

    refresh() {
        this.nodeService.refreshNodeInformation(this.ip).subscribe(node => {
            this.node = node;
        });
    }
}

