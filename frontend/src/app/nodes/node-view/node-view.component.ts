import { Component, OnInit } from '@angular/core';
import { Node, NodesService } from '../nodes.service';
import { ActivatedRoute } from '@angular/router';
import { CommonModule, JsonPipe } from '@angular/common';

@Component({
    selector: 'app-node-view',
    standalone: true,
    imports: [CommonModule, JsonPipe],
    templateUrl: './node-view.component.html',
    styleUrl: './node-view.component.css'
})
export class NodeViewComponent implements OnInit {

    node!: Node;

    constructor(
        private route: ActivatedRoute,
        private nodeService: NodesService
    ) { }

    ngOnInit(): void {
        this.route.paramMap.subscribe(params => {
            const ip = params.get('ip') ?? '';
            this.nodeService.getNode(ip).subscribe(node => {
                this.node = node;
            });
        });
    }
}
