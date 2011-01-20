# vim: set expandtab ts=4 sw=4 filetype=python:

import textwrap

class Chart(object):

    def __init__(self, chart_id=None, parent_id=None, title=None,
        theme_id=None, number_of_stars=None, stars_filled_in=None,
        created=None):

        self.chart_id = chart_id
        self.parent_id = parent_id
        self.title = title
        self.theme_id = theme_id
        self.number_of_stars = number_of_stars
        self.stars_filled_in = stars_filled_in
        self.created = created

    @property
    def stars(self):
        """
        Return a list of empty and filled-in stars.
        """

        if self.number_of_stars is None:
            raise ValueError("I need a number of stars!")

        if not self.stars_filled_in:
            return [self.empty_star] * self.number_of_stars

        else:

            return (
                [self.filled_in_star] * self.stars_filled_in
                + [self.empty_star] * (
                    self.number_of_stars - self.stars_filled_in))

    @property
    def all_done(self):

        return self.number_of_stars is not None \
        and self.number_of_stars == self.stars_filled_in

    @property
    def embedded_video(self):

        return textwrap.dedent("""
            <iframe title="YouTube video player" class="youtube-player"
            type="text/html" width="480" height="390"
            src="http://www.youtube.com/embed/MRm-wkDqSKY" frameborder="0"
            allowFullScreen></iframe>""")

    @property
    def empty_star(self):

        return textwrap.dedent("""
            <form action="/chart/%s/fill_in_a_star" method="POST">

                <input type="submit"
                    value=""
                    style="width:296px; height:181px; background:url(/static/sumo-grey.jpg);"
                />

            </form>""" % self.chart_id)

    @property
    def filled_in_star(self):

        return textwrap.dedent("""
            <img src="/static/sumo.jpg" width="296" height="176"
                alt="empty star"/>""")

    @classmethod
    def insert_sample_data(cls, dbconn):

        qry = textwrap.dedent("""
            insert into chart
            (title, number_of_stars)
            values
            (%s, %s)

            returning chart_id, parent_id, title, theme_id,
            number_of_stars, stars_filled_in, created
            """)

        cursor = dbconn.cursor()
        cursor.execute(qry, ['Charlie eats a good dinner', 5])

        return [cls(*row) for row in cursor.fetchall()]


    @classmethod
    def by_primary_key(cls, dbconn, chart_id):

        qry = textwrap.dedent("""
            select chart_id, parent_id, title, theme_id,
            number_of_stars, stars_filled_in, created

            from chart

            where chart_id = (%s)
            """)

        cursor = dbconn.cursor()
        cursor.execute(qry, [chart_id])
        results = cursor.fetchone()

        if results:
            return cls(*results)

    @classmethod
    def by_parent_id_and_title(cls, dbconn, parent_id, title):

        qry = textwrap.dedent("""
            select chart_id, parent_id, title, theme_id,
            number_of_stars, stars_filled_in, created

            from chart

            where parent_id = (%s)
            and title = (%s)
            """)

        cursor = dbconn.cursor()
        cursor.execute(qry, [parent_id, title])

        results = cursor.fetchone()

        if results:
            return cls(*results)

    def fill_in_a_star(self, dbconn):

        if not self.chart_id:
            raise ValueError("I need a chart ID!")

        if self.stars_filled_in == self.number_of_stars:
            raise ValueError("This chart is already done!")

        qry = textwrap.dedent("""
            update chart
            set stars_filled_in = stars_filled_in + 1
            where chart_id = (%s)
            returning chart_id, parent_id, title, theme_id,
            number_of_stars, stars_filled_in, created""")

        cursor = dbconn.cursor()
        cursor.execute(qry, [self.chart_id])

        (chart_id, parent_id, title, theme_id, number_of_stars,
            stars_filled_in, created) = cursor.fetchone()

        self.chart_id = chart_id
        self.parent_id = parent_id
        self.title = title
        self.theme_id = theme_id
        self.number_of_stars = number_of_stars
        self.stars_filled_in = stars_filled_in
        self.created = created

        return self


    def reset_chart(self, dbconn):

        if not self.chart_id:
            raise ValueError("I need a chart ID!")

        if self.stars_filled_in == 0:
            return self

        qry = textwrap.dedent("""
            update chart
            set stars_filled_in = 0
            where chart_id = (%s)
            returning chart_id, parent_id, title, theme_id,
            number_of_stars, stars_filled_in, created""")

        cursor = dbconn.cursor()
        cursor.execute(qry, [self.chart_id])

        (chart_id, parent_id, title, theme_id, number_of_stars,
            stars_filled_in, created) = cursor.fetchone()

        self.chart_id = chart_id
        self.parent_id = parent_id
        self.title = title
        self.theme_id = theme_id
        self.number_of_stars = number_of_stars
        self.stars_filled_in = stars_filled_in
        self.created = created

        return self

    @property
    def reset_button(self):

        return textwrap.dedent("""
            <form id="reset_button"
                action="/chart/%s/reset_chart"
            method="POST">
                <input type="submit" value="start over" />
            </form>""" % self.chart_id)

    @classmethod
    def insert_new_chart(cls, dbconn, parent_id, title, theme_id,
        number_of_stars):

        qry = textwrap.dedent("""
            insert into chart
            (parent_id, title, theme_id, number_of_stars)
            values
            (%s, %s, %s, %s)
            returning chart_id, parent_id, title, theme_id,
            number_of_stars, stars_filled_in, created""")

        cursor = dbconn.cursor()

        cursor.execute(qry,
            [parent_id, title, theme_id, number_of_stars])

        (chart_id, parent_id, title, theme_id, number_of_stars,
            stars_filled_in, created) = cursor.fetchone()

        self = cls()

        self.chart_id = chart_id
        self.parent_id = parent_id
        self.title = title
        self.theme_id = theme_id
        self.number_of_stars = number_of_stars
        self.stars_filled_in = stars_filled_in
        self.created = created

        return self


    @classmethod
    def from_parsed_post_data(cls, dbconn, parsed_post_data):

        """

        {'theme_id': ['-1'], 'number-of-stars': ['1'], 'parent_id': ['-1'],
        'title': ['title goes here']}

        """

        parent_id = int(parsed_post_data['parent_id'][0])
        title = parsed_post_data['title'][0]
        theme_id = int(parsed_post_data['theme_id'][0])
        number_of_stars = int(parsed_post_data['number-of-stars'][0])

        if title == 'title goes here':
            raise ValueError("Sorry, you need a better title",
                dict(parent_id=parent_id, title=title, theme_id=theme_id,
                number_of_stars=number_of_stars))

        # While I don't have theming or authentication, just insert
        # NULLs for parent_id and theme_id.
        if parent_id == -1:
            parent_id = None

        if theme_id == -1:
            theme_id = None

        return cls.insert_new_chart(dbconn, parent_id, title, theme_id,
            number_of_stars)

