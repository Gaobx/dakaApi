# -*- coding: utf-8 -*-

import config
import pymysql


class sql(object):
    def __init__(self):
        self.db = pymysql.connect(config.mql_url,
                                  config.mql_user,
                                  config.mql_pswd,
                                  config.mql_db,
                                  charset = "utf8")

        self.cursor = self.db.cursor()

    def login(self, user_id):
        """
        :param user_id: 用户微信号，作为主键
        :return: 
            若是新用户，return {'code': '1001', 'msg':'creat new user successfully'}
            若已存在用户，return {'code':'1002', 'msg':'login in successfully'}
        """
        sql_login = "select * \
                    from user_info \
                    where user_id = '%s'" % (user_id)

        sql_create = "insert into user_info(user_id) values ('%s')" % (user_id)

        try:
            self.cursor.execute(sql_login)
            result = self.cursor.fetchall()
            if len(result) != 0:
                return {'code': '1002', 'msg': 'login in successfully'}

            result = self.cursor.execute(sql_create)
            # print(result)

            self.db.commit()
            return {'code': '1001', 'msg': 'creat new user successfully'}

        except BaseException as e:
            print(e)
            self.db.rollback()
            return False

    def get_slide_images(self):
        """
        返回滑动图片url
        :return: 
        """
        sql = "select option_value \
                from config \
                where option_name REGEXP '%s'" % ('slide_image_')

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            print(result)
            return result
        except BaseException as e:
            print(e)
            return False

    def create_group(self, params):
        """
        :param params: some info
        :return: 
        """
        print(params)
        if 'group_image' in params:
            sql_gp_info = "insert into group_info( \
                        group_id, group_image, create_date, group_intro, \
                        money, member_num, limit_num, duration, type) \
                        values \
                        (default, %s, now(), %s, %d, 1, %d, %d, %s)" % \
                        ( params['group_image'], params['group_intro'],
                          params['money'], params['limit_num'],
                          params['duration'], params['type'])
        else:

            sql_gp_info = "insert into group_info( \
                        group_id, create_date, group_intro, \
                        money, member_num, limit_num, duration, \
                        is_finished, type) \
                        values \
                        (default, now(), '%s', %d, 1, %d, %d, 'no', '%s')" % \
                          (params['group_intro'],
                           int(params['money']), int(params['limit_num']),
                           int(params['duration']),
                           params['type'])

        try:
            self.cursor.execute(sql_gp_info)
            gp_id = self.cursor.execute("SELECT LAST_INSERT_ID()")
            sql_gp_usr = "insert into group_user(group_id, user_id, is_creater) \
                                values(%d, '%s', '%s')" % (gp_id, params['user_id'], 'yes')
            self.cursor.execute(sql_gp_usr)

            self.db.commit()

            return {'code': '1007', 'msg': 'create group successfully'}
        except BaseException as e:
            print(e)
            return {'code': '1006', 'msg': 'create group failed'}






