# Setting Up RPM Builds in Konflux (Example)

Start by reviewing the [Fedora onboarding guide][onboarding].

## Steps

1.  You'll need to create a repository similar to this one, intending to host a
    **dist-git-like repository** (e.g., [Fedora's cpio][cpio]).

2.  You must either **[create][mr]** or have a pre-created Konflux tenant. (This
    is generally the most complicated step.)

3.  You need to grant the **[Konflux app][konflux app]** access to this
    repository.

4.  Finally, create a new **component** within your **[tenant and
    application][tenant]**.

5.  Open your RPM specific PR.

[cpio]: https://src.fedoraproject.org/rpms/cpio
[mr]: https://gitlab.com/fedora/infrastructure/konflux/tenants-config/-/merge_requests/31/diffs
[konflux app]: https://github.com/apps/konflux-fedora
[onboarding]: https://gitlab.com/fedora/infrastructure/konflux/rpmbuild-pipeline/-/blob/main/docs/onboarding.md?ref_type=heads
[tenant]: https://konflux.fedoraproject.org/ns/fedora-on-konflux-tenant/applications
