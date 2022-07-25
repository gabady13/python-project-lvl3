"""Progress Spinner."""

from progress.spinner import PixelSpinner


class ProgressSpinner(PixelSpinner):
    """Progress Class."""

    def update(self):
        """Update."""
        index = self.index % len(self.phases)
        line = ' '.join([self.phases[index], self.message])
        self.writeln(line)

    def finish(self):
        """Finish progress."""
        line = ' '.join(['*', self.message])
        print('\r{0}'.format(line), file=self.file)
