<script>
    import '@evidence-dev/tailwind/fonts.css';
    import '../app.css';
    import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
    export let data;
</script>

<EvidenceDefaultLayout fullWidth=true hideSidebar=true githubRepo="https://github.com/yteraoka/amazon-price-watcher" {data}>
    <slot slot="content" />
</EvidenceDefaultLayout>
